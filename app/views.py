from django.shortcuts import render

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, Objetivo, Subtarefa

class CriarUsuarioView(View):
    def get(self, request):
        return render(request, 'criar_usuario.html')

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
    
class CriarObjetivoView(View):
    def get(self, request):
        return render(request, 'criar_objetivo.html')

    def post(self, request):
        nome_objetivo = request.POST.get('nome_objetivo')
        descricao_objetivo = request.POST.get('descricao_objetivo')
        subtarefas_nomes = request.POST.getlist('subtarefa_nome')
        subtarefas_descricoes = request.POST.getlist('subtarefa_descricao')

        usuario = Usuario.objects.first()

        if not nome_objetivo:
            messages.error(request, 'É necessário preencher o nome do objetivo.')
            return redirect('criar_objetivo')

        objetivo = Objetivo.objects.create(
            Nome=nome_objetivo,
            Descrição=descricao_objetivo,
            Status='pendente',  # Estado inicial é "pendente"
            usuario=usuario
        )

        count = 0
        for i in range(len(subtarefas_nomes)):
            nome = subtarefas_nomes[i]
            descricao = subtarefas_descricoes[i]

            if nome.strip():
                Subtarefa.objects.create(
                    Nome=nome,
                    descrição=descricao,
                    Status='pendente',  # Estado inicial é "pendente"
                    objetivo=objetivo
                )
                count += 1

        messages.success(
            request,
            f'Objetivo "{nome_objetivo}" foi criado com sucesso com {count} subtarefa(s).'
        )
        return redirect('criar_objetivo')

class VisualizarObjetivosView(View):
    def get(self, request):

        usuario = Usuario.objects.first()
        
        if not usuario:
            messages.error(request, "Nenhum usuário encontrado. Por favor, crie um usuário primeiro.")
            return redirect('criar_usuario')
            
        filtro = request.GET.get('filtro', 'todos')
        
        if filtro == 'pendentes':
            objetivos = Objetivo.objects.filter(usuario=usuario, Status='pendente')
        elif filtro == 'ativas':
            objetivos = Objetivo.objects.filter(usuario=usuario, Status='ativa')
        elif filtro == 'completas':
            objetivos = Objetivo.objects.filter(usuario=usuario, Status='completa')
        else: 
            objetivos = Objetivo.objects.filter(usuario=usuario)
        
        
        context = {
            'objetivos': objetivos,
            'filtro_atual': filtro
        }
        
        return render(request, 'visualizar_objetivos.html', context)
