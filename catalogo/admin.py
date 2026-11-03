from django.contrib import admin

from avaliacoes.admin import ReviewInline

from .models import Cafe, Marca


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("nome", "pais_origem", "site_oficial", "criado_em")
    search_fields = ("nome", "pais_origem")


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "marca",
        "tipo_grao",
        "tipo_torra",
        "intensidade",
        "destaque",
        "exibir_nota_media",
    )
    list_filter = ("tipo_grao", "tipo_torra", "destaque", "marca")
    search_fields = ("nome", "marca__nome", "notas_aromaticas", "origem_grao")
    list_editable = ("destaque",)
    inlines = (ReviewInline,)

    @admin.display(description="Nota Média")
    def exibir_nota_media(self, obj):
        return obj.nota_media
