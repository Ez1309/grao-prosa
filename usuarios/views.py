from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import TipoTorra, TipoPerfil

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
    Cadastro de novos usuários e inicialização do Perfil.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        usuario = request.POST.get('usuario', '').strip()
        email = request.POST.get('email', '').strip().lower()
        senha = request.POST.get('senha', '')
        confirmar_senha = request.POST.get('confirmar_senha', '')
        torra_preferida = request.POST.get('torra_preferida', '')

        context = {
            'tipo_torra_choices': TipoTorra.choices,
            'nome': nome,
            'usuario': usuario,
            'email': email,
            'torra_preferida': torra_preferida,
        }

        # 1. Validação de senhas coincidentes
        if senha != confirmar_senha:
            messages.error(request, "As senhas digitadas não coincidem.")
            return render(request, 'usuarios/cadastro.html', context)

        # 2. Validação de tamanho mínimo
        if len(senha) < 6:
            messages.error(request, "A senha deve conter no mínimo 6 caracteres.")
            return render(request, 'usuarios/cadastro.html', context)

        # 3. Validação de unicidade do nome de usuário
        if User.objects.filter(username__iexact=usuario).exists():
            messages.error(request, f"O nome de usuário '{usuario}' já está cadastrado. Por favor, escolha outro.")
            return render(request, 'usuarios/cadastro.html', context)

        # 4. Validação de unicidade do e-mail
        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, f"O e-mail '{email}' já está em uso. Tente fazer login.")
            return render(request, 'usuarios/cadastro.html', context)

        # 5. Criação do Usuário
        user = User.objects.create_user(
            username=usuario,
            email=email,
            password=senha,
            first_name=nome
        )

        # 6. Atualização do Perfil (criado automaticamente pelo signal post_save)
        if hasattr(user, 'perfil'):
            user.perfil.tipo_perfil = TipoPerfil.ENTUSIASTA
            if torra_preferida:
                user.perfil.torra_preferida = torra_preferida
            user.perfil.save()

        # 7. Autenticação imediata pós-cadastro
        login(request, user)
        nome_exibicao = nome or usuario
        messages.success(request, f"Conta criada com sucesso! Seja muito bem-vindo(a) ao Grão & Prosa, {nome_exibicao}!")
        return redirect('home')

    context = {
        'tipo_torra_choices': TipoTorra.choices,
    }
    return render(request, 'usuarios/cadastro.html', context)
