from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("cafe", "usuario", "nota", "data_avaliacao")
    list_filter = ("nota", "data_avaliacao")
    search_fields = ("cafe__nome", "usuario__username", "comentario")
    date_hierarchy = "data_avaliacao"


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ("data_avaliacao",)
