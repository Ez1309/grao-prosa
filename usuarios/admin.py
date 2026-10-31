from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Perfil


class PerfilInline(admin.StackedInline):
    """
    Permite visualizar e editar as informações do Perfil
    diretamente na página de edição do Usuário.
    """
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil de Café'
    fk_name = 'usuario'


# Re-registra o UserAdmin padrão do Django para incluir o PerfilInline
class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    """
    Registro individual do Perfil com filtros e busca avançada.
    """
    list_display = ('usuario', 'tipo_perfil', 'torra_preferida', 'criado_em')
    list_filter = ('tipo_perfil', 'torra_preferida')
    search_fields = ('usuario__username', 'usuario__email', 'bio')
    ordering = ('-criado_em',)
