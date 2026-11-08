"""
URL configuration for grao_prosa project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('usuarios/', include('usuarios.urls')),
]

# Handlers padrão de erro HTTP para produção (DEBUG=False)
handler404 = 'grao_prosa.views.erro_404'
handler500 = 'grao_prosa.views.erro_500'
handler403 = 'grao_prosa.views.erro_403'
handler400 = 'grao_prosa.views.erro_400'

# Em ambiente de desenvolvimento, disponibiliza rotas para pré-visualização das telas de erro
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('erros/404/', views.erro_404, name='preview_404'),
        path('erros/500/', views.erro_500, name='preview_500'),
        path('erros/403/', views.erro_403, name='preview_403'),
        path('erros/400/', views.erro_400, name='preview_400'),
    ]

