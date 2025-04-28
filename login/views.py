from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Usuario
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.template import RequestContext

class CriarUsuarioView(View):
    def get(self, request):
        return render(request, 'login/criar_usuario.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not username or not email or not senha:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request,'login/criar_usuario.html')

        elif Usuario.objects.filter(E_mail=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return render(request,'login/criar_usuario.html')
        
        elif Usuario.objects.filter(Username=username).exists():
            messages.error(request, 'Este usuário já está cadastrado.')
            return render(request,'login/criar_usuario.html')

        else:
            # Usar make_password para criar senha hasheada
            senha_hasheada = make_password(senha)
            Usuario.objects.create(Username=username, E_mail=email, Senha=senha_hasheada)
            return redirect('logar')  # MUDANÇA AQUI: usar redirect em vez de render

class LoginView(View):
    def get(self, request):
        return render(request, 'login/logar.html')

    def post(self, request):
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not email or not senha:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request, 'login/logar.html')

        try:
            usuario = Usuario.objects.get(E_mail=email)
            # Usar check_password para verificar a senha hasheada
            if check_password(senha, usuario.Senha):
                request.session['usuario_id'] = usuario.id
                request.session.save()  # Forçar a gravação da sessão
                # Redirecionar para a view de visualização de objetivos
                return redirect('visualizar_objetivos')
            else:
                messages.error(request, 'Senha incorreta.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')

        return render(request, 'login/logar.html')

class LogoutView(View):
    def get(self, request):
        # Remover o ID do usuário da sessão
        if 'usuario_id' in request.session:
            del request.session['usuario_id']
        
        return redirect('logar')  # Redireciona para a URL de login