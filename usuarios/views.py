from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    """
    Autenticação de usuários primariamente por E-mail (com fallback para username).
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email_ou_usuario = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '')

        user_obj = User.objects.filter(email__iexact=email_ou_usuario).first()
        if not user_obj:
            user_obj = User.objects.filter(username__iexact=email_ou_usuario).first()

        user = None
        if user_obj:
            user = authenticate(request, username=user_obj.username, password=senha)

        if user is not None:
            login(request, user)
            nome_exibicao = user.first_name or user.username
            messages.success(request, f"Olá, {nome_exibicao}! Bem-vindo(a) ao Grão & Prosa.")
            next_url = request.POST.get('next') or request.GET.get('next')
            return redirect(next_url or 'home')
        else:
            messages.error(request, "E-mail ou senha inválidos. Por favor, verifique suas credenciais.")
            return render(request, 'usuarios/login.html', {'email': email_ou_usuario})

    return render(request, 'usuarios/login.html')

def logout_view(request):
    """
    Encerramento seguro da sessão do usuário.
    """
    logout(request)
    messages.info(request, "Sua sessão foi encerrada com sucesso. Até breve!")
    return redirect('home')

def cadastro_view(request):
    """
    Cadastro de novos usuários (preparação para a próxima etapa).
    """
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'usuarios/cadastro.html')
