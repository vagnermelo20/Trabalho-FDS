from django.shortcuts import render

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
from django.http import HttpResponse

class CriarUsuarioView(View):
    def get(self, request):
        return render(request,'login/criar_usuario.html')

    def post(self, request):
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not nome or not email or not senha:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('login/criar_usuario.html')

        elif Usuario.objects.filter(E_mail=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return redirect('login/criar_usuario,html')

        else:
            Usuario.objects.create(Nome=nome, E_mail=email, Senha=senha)
            messages.success(request, f'Usuário "{nome}" criado com sucesso!')
            return redirect('login/logar.html')  # Redirecionar para página de login após criação

class LoginView(View):
    def get(self, request):
        return render(request, 'login/logar.html')
    
    def post(self, request):
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not email or not senha:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('login/logar.html')

        try:
            usuario = Usuario.objects.get(E_mail=email)
            if usuario.Senha == senha:
                request.session['usuario_id'] = usuario.id
                messages.success(request, f'Bem-vindo(a), {usuario.Nome}!')
                return redirect('objetivos/objetivos/visualizar_objetivos.html')  # Redireciona para visualização após login
            else:
                messages.error(request, 'Senha incorreta.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')

        return redirect('login')

class LogoutView(View):
    def get(self, request):
        # Remover o ID do usuário da sessão
        if 'usuario_id' in request.session:
            del request.session['usuario_id']
        
        messages.success(request, "Você saiu do sistema com sucesso.")
        return redirect('login/logar.html')