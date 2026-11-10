from django.urls import path

from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:cafe_id>/', views.detalhes_cafe, name='detalhes_cafe'),
]