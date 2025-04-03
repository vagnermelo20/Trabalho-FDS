from django.shortcuts import render

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, Objetivo, Subtarefa
from django.http import HttpResponse

class CriarUsuarioView(View):
    def get(self, request):
        return HttpResponse('<h1>TO NA HOME<h1>')

    def post(self, request):
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not nome or not email or not senha:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('criar_usuario')

        if Usuario.objects.filter(E_mail=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return redirect('criar_usuario')

        Usuario.objects.create(Nome=nome, E_mail=email, Senha=senha)
        messages.success(request, f'Usuário "{nome}" criado com sucesso!')
        return redirect('criar_usuario')
    

