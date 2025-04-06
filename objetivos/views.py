from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Objetivo, Subtarefa
from login.models import Usuario

class CriarObjetivoView(View):
    def get(self, request):
        # Verificar se o usuário está logado
        if 'usuario_id' not in request.session:
            messages.error(request, "Você precisa estar logado para criar objetivos.")
            return redirect('logar')

        # Renderiza o formulário de criação de objetivo
        return render(request, 'objetivos/criar_objetivo.html')

    def post(self, request):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para criar objetivos.")
            return redirect('logar')

        # Obter os dados do formulário
        nome_objetivo = request.POST.get('nome_objetivo')
        descricao_objetivo = request.POST.get('descricao_objetivo')

        # Validar o nome do objetivo
        if not nome_objetivo:
            messages.error(request, 'É necessário preencher o nome do objetivo.')
            return render(request, 'objetivos/criar_objetivo.html')

        # Verificar se já existe um objetivo com o mesmo nome para este usuário
        if Objetivo.objects.filter(Nome=nome_objetivo, usuario_id=usuario_id).exists():
            messages.error(request, 'Você já tem uma tarefa com este nome. Por favor, escolha um nome diferente.')
            return render(request, 'objetivos/criar_objetivo.html', {
                'nome_objetivo': nome_objetivo,
                'descricao_objetivo': descricao_objetivo
            })

        # Criar o objetivo associado ao usuário logado
        Objetivo.objects.create(
            Nome=nome_objetivo,
            Descrição=descricao_objetivo,
            Status='pendente',
            usuario_id=usuario_id  # Associar ao usuário logado
        )

        return redirect('visualizar_objetivos')


class VisualizarObjetivosView(View):
    def get(self, request):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para visualizar seus objetivos.")
            return redirect('logar')

        # Buscar todos os objetivos do usuário logado
        objetivos = Objetivo.objects.filter(usuario_id=usuario_id)

        context = {
            'objetivos': objetivos,
        }

        return render(request, 'objetivos/visualizar_objetivos.html', context)


class DeletarObjetivoView(View):
    def post(self, request, objetivo_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para excluir objetivos.")
            return redirect('logar')

        # Buscar o objetivo e verificar se pertence ao usuário logado
        objetivo = get_object_or_404(Objetivo, id=objetivo_id, usuario_id=usuario_id)

        nome_objetivo = objetivo.Nome
        objetivo.delete()

        return redirect('visualizar_objetivos')


class EditarObjetivoView(View):
    def get(self, request, objetivo_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para editar objetivos.")
            return redirect('logar')

        objetivo = get_object_or_404(Objetivo, id=objetivo_id, usuario_id=usuario_id)

        context = {
            'objetivo': objetivo,
        }

        return render(request, 'objetivos/editar_objetivo.html', context)

    def post(self, request, objetivo_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para editar objetivos.")
            return redirect('logar')

        objetivo = get_object_or_404(Objetivo, id=objetivo_id, usuario_id=usuario_id)

        nome_objetivo = request.POST.get('nome_objetivo')
        descricao_objetivo = request.POST.get('descricao_objetivo')
        novo_status = request.POST.get('status')

        # Validar o nome do objetivo
        if not nome_objetivo:
            messages.error(request, 'É necessário preencher o nome do objetivo.')
            return render(request, 'objetivos/editar_objetivo.html', {'objetivo': objetivo})

        # Verificar se já existe OUTRO objetivo com o mesmo nome para este usuário
        # Usamos exclude(id=objetivo_id) para não considerar o próprio objetivo na verificação
        if Objetivo.objects.filter(Nome=nome_objetivo, usuario_id=usuario_id).exclude(id=objetivo_id).exists():
            messages.error(request, 'Você já tem uma tarefa com este nome. Por favor, escolha um nome diferente.')
            return render(request, 'objetivos/editar_objetivo.html', {
                'objetivo': objetivo,
                'nome_objetivo': nome_objetivo,
                'descricao_objetivo': descricao_objetivo
            })

        objetivo.Nome = nome_objetivo
        objetivo.Descrição = descricao_objetivo
        objetivo.Status = novo_status
        objetivo.save()

        return redirect('visualizar_objetivos')