from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


class Marca(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Marca")
    pais_origem = models.CharField(
        max_length=100, default="Brasil", verbose_name="País de Origem"
    )
    historia = models.TextField(blank=True, verbose_name="História / Descrição")
    site_oficial = models.URLField(blank=True, verbose_name="Site Oficial")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.nome


class Cafe(models.Model):
    class TipoGrao(models.TextChoices):
        ARABICA = "ARABICA", "100% Arábica"
        ROBUSTA = "ROBUSTA", "Robusta / Conilon"
        BLEND = "BLEND", "Blend Especial"

    class TipoTorra(models.TextChoices):
        CLARA = "CLARA", "Torra Clara"
        MEDIA = "MEDIA", "Torra Média"
        ESCURA = "ESCURA", "Torra Escura"

    nome = models.CharField(max_length=150, verbose_name="Nome do Café")
    marca = models.ForeignKey(
        Marca, on_delete=models.CASCADE, related_name="cafes", verbose_name="Marca"
    )
    tipo_grao = models.CharField(
        max_length=15,
        choices=TipoGrao.choices,
        default=TipoGrao.ARABICA,
        verbose_name="Tipo de Grão",
    )
    tipo_torra = models.CharField(
        max_length=10,
        choices=TipoTorra.choices,
        default=TipoTorra.MEDIA,
        verbose_name="Ponto de Torra",
    )
    intensidade = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
        verbose_name="Intensidade (1 a 10)",
    )
    notas_aromaticas = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Notas Sensoriais",
        help_text="Ex: Caramelo, chocolate amargo, frutas vermelhas",
    )
    origem_grao = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Região de Origem",
        help_text="Ex: Sul de Minas, Mogiana Paulista, Cerrado",
    )
    descricao = models.TextField(verbose_name="Descrição do Produto")
    imagem = models.ImageField(
        upload_to="cafes/", blank=True, null=True, verbose_name="Capa / Imagem do Café"
    )
    destaque = models.BooleanField(default=False, verbose_name="Café em Destaque?")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Café"
        verbose_name_plural = "Cafés"

    def __str__(self):
        return f"{self.nome} ({self.marca.nome})"

    @property
    def nota_media(self):
        # A relação 'avaliacoes' será criada no Bloco 2 com o app 'avaliacoes'
        media = self.avaliacoes.aggregate(Avg("nota"))["nota__avg"]
        return round(media, 1) if media else 0.0

    @property
    def total_avaliacoes(self):
        return self.avaliacoes.count()
