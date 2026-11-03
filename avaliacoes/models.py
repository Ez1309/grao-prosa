from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from catalogo.models import Cafe


class Review(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews", verbose_name="Avaliador"
    )
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name="avaliacoes",
        verbose_name="Café Avaliado",
    )
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Nota (1 a 5 estrelas)",
    )
    comentario = models.TextField(verbose_name="Comentário sobre o Café")
    data_avaliacao = models.DateTimeField(
        auto_now_add=True, verbose_name="Data da Avaliação"
    )

    class Meta:
        unique_together = ("usuario", "cafe")
        ordering = ("-data_avaliacao",)
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    def __str__(self):
        return f"Avaliação de {self.usuario.username} para {self.cafe.nome}"
