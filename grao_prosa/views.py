from django.shortcuts import render


def erro_404(request, exception=None):
    """Página de Erro 404 - Página Não Encontrada."""
    return render(request, '404.html', status=404)


def erro_500(request):
    """Página de Erro 500 - Erro Interno do Servidor."""
    return render(request, '500.html', status=500)


def erro_403(request, exception=None):
    """Página de Erro 403 - Acesso Negado / Proibido."""
    return render(request, '403.html', status=403)


def erro_400(request, exception=None):
    """Página de Erro 400 - Requisição Inválida."""
    return render(request, '400.html', status=400)
