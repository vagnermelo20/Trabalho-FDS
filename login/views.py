from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Usuario
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

class CriarUsuarioView(View):
    def get(self, request):
        return render(request, 'login/criar_usuario.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not username or not email or not senha:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('criar_usuario')  # Corrigido para usar nome de URL

        elif Usuario.objects.filter(E_mail=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return redirect('criar_usuario')
        
        elif Usuario.objects.filter(Username=username).exists():  # Corrigido para usar Username
            messages.error(request, 'Este usuário já está cadastrado.')
            return redirect('criar_usuario')

        else:
            # Usar make_password para criar senha hasheada
            senha_hasheada = make_password(senha)
            Usuario.objects.create(Username=username, E_mail=email, Senha=senha_hasheada)
            messages.success(request, f'Usuário "{username}" criado com sucesso!')
            return redirect('logar')  # Corrigido para usar nome de URL

class LoginView(View):
    def get(self, request):
        return render(request, 'login/logar.html')
    
    def post(self, request):
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not email or not senha:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('logar')  # Corrigido para usar nome de URL

        try:
            usuario = Usuario.objects.get(E_mail=email)
            # Usar check_password para verificar a senha hasheada
            if check_password(senha, usuario.Senha):
                request.session['usuario_id'] = usuario.id
                messages.success(request, f'Bem-vindo(a), {usuario.Username}!')
                return redirect('visualizar_objetivos')
            else:
                messages.error(request, 'Senha incorreta.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')

        return redirect('logar')  # Corrigido para usar nome de URL

class LogoutView(View):
    def get(self, request):
        # Remover o ID do usuário da sessão
        if 'usuario_id' in request.session:
            del request.session['usuario_id']
        
        messages.success(request, "Você saiu do sistema com sucesso.")
        return redirect('logar')  # Corrigido para usar nome de URL