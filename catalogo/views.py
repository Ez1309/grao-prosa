from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from avaliacoes.forms import ReviewForm

from .forms import CafeForm, MarcaForm
from .models import Cafe


def eh_especialista(user):
    """
    Função de validação para o decorador @user_passes_test.
    Garante acesso apenas para usuários com tipo_perfil ESPECIALISTA (ou staff/admin).
    """
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.is_staff
            or (hasattr(user, "perfil") and user.perfil.tipo_perfil == "ESPECIALISTA")
        )
    )


def index(request):
    query = request.GET.get("q", "").strip()
    torra_filtro = request.GET.get("torra", "")
    grao_filtro = request.GET.get("grao", "")

    cafes = Cafe.objects.select_related("marca").all()

    if query:
        cafes = cafes.filter(
            Q(nome__icontains=query)
            | Q(marca__nome__icontains=query)
            | Q(notas_aromaticas__icontains=query)
            | Q(origem_grao__icontains=query)
        )

    if torra_filtro:
        cafes = cafes.filter(tipo_torra=torra_filtro)
    if grao_filtro:
        cafes = cafes.filter(tipo_grao=grao_filtro)

    context = {
        "cafes": cafes,
        "busca": query,
        "torra_filtro": torra_filtro,
        "grao_filtro": grao_filtro,
        "tipos_torra": Cafe.TipoTorra.choices,
        "tipos_grao": Cafe.TipoGrao.choices,
    }
    return render(request, "catalogo/index.html", context)


def detalhes_cafe(request, cafe_id):
    cafe = get_object_or_404(Cafe.objects.select_related("marca"), id=cafe_id)
    avaliacoes = cafe.avaliacoes.select_related("usuario", "usuario__perfil").all()
    usuario_ja_avaliou = False
    form = None

    if request.user.is_authenticated:
        usuario_ja_avaliou = cafe.avaliacoes.filter(usuario=request.user).exists()

        if request.method == "POST":
            if usuario_ja_avaliou:
                messages.warning(
                    request, "Você já enviou uma avaliação para este café."
                )
                return redirect("catalogo:detalhes_cafe", cafe_id=cafe.id)

            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.usuario = request.user
                review.cafe = cafe
                review.save()
                messages.success(request, "Avaliação enviada com sucesso!")
                return redirect("catalogo:detalhes_cafe", cafe_id=cafe.id)
        else:
            form = ReviewForm()
    elif request.method == "POST":
        messages.error(request, "Você precisa estar conectado para avaliar este café.")
        return redirect("usuarios:login")

    context = {
        "cafe": cafe,
        "avaliacoes": avaliacoes,
        "form": form,
        "usuario_ja_avaliou": usuario_ja_avaliou,
    }
    return render(request, "catalogo/detalhes_cafe.html", context)


@user_passes_test(eh_especialista, login_url="usuarios:login")
def criar_marca(request):
    """
    Área de Curadoria: Permite ao Especialista cadastrar uma nova Marca.
    """
    if request.method == "POST":
        form = MarcaForm(request.POST)
        if form.is_valid():
            marca = form.save()
            messages.success(
                request, f"Marca '{marca.nome}' cadastrada com sucesso na curadoria!"
            )
            return redirect("catalogo:criar_cafe")
    else:
        form = MarcaForm()

    return render(request, "catalogo/form_marca.html", {"form": form})


@user_passes_test(eh_especialista, login_url="usuarios:login")
def criar_cafe(request):
    """
    Área de Curadoria: Permite ao Especialista cadastrar um novo Café.
    """
    if request.method == "POST":
        form = CafeForm(request.POST, request.FILES)
        if form.is_valid():
            cafe = form.save()
            messages.success(
                request, f"Café '{cafe.nome}' cadastrado com sucesso no catálogo!"
            )
            return redirect("catalogo:detalhes_cafe", cafe_id=cafe.id)
    else:
        form = CafeForm()

    return render(request, "catalogo/form_cafe.html", {"form": form})
