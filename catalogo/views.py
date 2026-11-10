from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from avaliacoes.forms import ReviewForm
from avaliacoes.models import Review

from .forms import CafeForm, MarcaForm
from .models import Cafe, Marca


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


@login_required(login_url="usuarios:login")
def dashboard(request):
    """
    Bloco 4: Dashboard Analítico com métricas gerenciais e gráficos interativos Chart.js.
    Apresenta KPIs consolidados, distribuição por torra, top 5 cafés avaliados e histograma de notas.
    """
    # Métricas Executivas (KPIs)
    total_cafes = Cafe.objects.count()
    total_marcas = Marca.objects.count()
    total_avaliacoes = Review.objects.count()
    media_geral_agg = Review.objects.aggregate(Avg("nota"))["nota__avg"]
    media_geral = round(media_geral_agg, 1) if media_geral_agg else 0.0

    # 1. Distribuição de Cafés por Ponto de Torra (Donut Chart)
    torra_counts = (
        Cafe.objects.values("tipo_torra")
        .annotate(total=Count("id"))
        .order_by("tipo_torra")
    )
    torra_dict = {item["tipo_torra"]: item["total"] for item in torra_counts}
    torra_labels = [label for _, label in Cafe.TipoTorra.choices]
    torra_data = [torra_dict.get(key, 0) for key, _ in Cafe.TipoTorra.choices]

    # 2. Top 5 Cafés Mais Bem Avaliados (Bar Chart)
    top_cafes_qs = (
        Cafe.objects.select_related("marca")
        .annotate(
            media_nota=Avg("avaliacoes__nota"),
            total_revs=Count("avaliacoes"),
        )
        .filter(total_revs__gt=0)
        .order_by("-media_nota", "-total_revs", "nome")[:5]
    )
    top_cafes_labels = [f"{c.nome} ({c.marca.nome})" for c in top_cafes_qs]
    top_cafes_medias = [round(float(c.media_nota), 1) for c in top_cafes_qs]
    top_cafes_totais = [c.total_revs for c in top_cafes_qs]

    # 3. Histograma de Notas (1 a 5 estrelas)
    notas_counts = (
        Review.objects.values("nota")
        .annotate(total=Count("id"))
        .order_by("nota")
    )
    notas_dict = {item["nota"]: item["total"] for item in notas_counts}
    histograma_labels = ["1 Estrela", "2 Estrelas", "3 Estrelas", "4 Estrelas", "5 Estrelas"]
    histograma_data = [notas_dict.get(n, 0) for n in range(1, 6)]

    # 4. Distribuição por Tipo de Grão (Complementar para Donut/Polar)
    grao_counts = (
        Cafe.objects.values("tipo_grao")
        .annotate(total=Count("id"))
        .order_by("tipo_grao")
    )
    grao_dict = {item["tipo_grao"]: item["total"] for item in grao_counts}
    grao_labels = [label for _, label in Cafe.TipoGrao.choices]
    grao_data = [grao_dict.get(key, 0) for key, _ in Cafe.TipoGrao.choices]

    dashboard_json = {
        "torra": {
            "labels": torra_labels,
            "data": torra_data,
        },
        "top_cafes": {
            "labels": top_cafes_labels,
            "medias": top_cafes_medias,
            "totais": top_cafes_totais,
        },
        "histograma": {
            "labels": histograma_labels,
            "data": histograma_data,
        },
        "grao": {
            "labels": grao_labels,
            "data": grao_data,
        },
    }

    context = {
        "total_cafes": total_cafes,
        "total_marcas": total_marcas,
        "total_avaliacoes": total_avaliacoes,
        "media_geral": media_geral,
        "top_cafes_lista": top_cafes_qs,
        "dashboard_data": dashboard_json,
    }
    return render(request, "catalogo/dashboard.html", context)

