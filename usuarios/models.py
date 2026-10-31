from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class TipoPerfil(models.TextChoices):
    ENTUSIASTA = 'ENTUSIASTA', 'Consumidor / Entusiasta'
    ESPECIALISTA = 'ESPECIALISTA', 'Especialista / Barista'


class TipoTorra(models.TextChoices):
    CLARA = 'CLARA', 'Torra Clara'
    MEDIA = 'MEDIA', 'Torra Média'
    ESCURA = 'ESCURA', 'Torra Escura'


class Perfil(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name="Usuário"
    )
    foto_avatar = models.ImageField(
        upload_to='avatares/',
        blank=True,
        null=True,
        verbose_name="Foto de Perfil"
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Biografia"
    )
    tipo_perfil = models.CharField(
        max_length=20,
        choices=TipoPerfil.choices,
        default=TipoPerfil.ENTUSIASTA,
        verbose_name="Tipo de Perfil"
    )
    torra_preferida = models.CharField(
        max_length=10,
        choices=TipoTorra.choices,
        blank=True,
        verbose_name="Torra Preferida"
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"
        ordering = ['-criado_em']

    def __str__(self):
        return f"Perfil de {self.usuario.username} ({self.get_tipo_perfil_display()})"


@receiver(post_save, sender=User)
def criar_ou_atualizar_perfil_usuario(sender, instance, created, **kwargs):
    """
    Signal (Gatilho) para criar automaticamente o Perfil sempre que um novo
    User for salvo no banco (inclusive superusuários criados via CLI).
    """
    if created:
        Perfil.objects.create(usuario=instance)
    else:
        if hasattr(instance, 'perfil'):
            instance.perfil.save()
