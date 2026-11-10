from django.urls import path

from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('marca/nova/', views.criar_marca, name='criar_marca'),
    path('cafe/novo/', views.criar_cafe, name='criar_cafe'),
    path('<int:cafe_id>/', views.detalhes_cafe, name='detalhes_cafe'),
]
