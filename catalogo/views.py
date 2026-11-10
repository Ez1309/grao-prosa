from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from avaliacoes.forms import ReviewForm

from .models import Cafe


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
