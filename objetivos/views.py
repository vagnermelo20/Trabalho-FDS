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

        # Criar o objetivo associado ao usuário logado
        Objetivo.objects.create(
            Nome=nome_objetivo,
            Descrição=descricao_objetivo,
            Status='pendente',
            usuario_id=usuario_id  # Associar ao usuário logado
        )

        messages.success(request, f'Objetivo "{nome_objetivo}" foi criado com sucesso!')
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

        messages.success(request, f'Objetivo "{nome_objetivo}" foi excluído com sucesso.')
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

        if not nome_objetivo:
            messages.error(request, 'É necessário preencher o nome do objetivo.')
            return redirect('editar_objetivo', objetivo_id=objetivo_id)

        objetivo.Nome = nome_objetivo
        objetivo.Descrição = descricao_objetivo
        objetivo.Status = novo_status
        objetivo.save()

        messages.success(request, f'Objetivo "{nome_objetivo}" atualizado com sucesso.')
        return redirect('visualizar_objetivos')


class EditarSubtarefaView(View):
    def get(self, request, subtarefa_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para editar subtarefas.")
            return redirect('logar')

        subtarefa = get_object_or_404(Subtarefa, id=subtarefa_id, objetivo__usuario_id=usuario_id)

        context = {
            'subtarefa': subtarefa,
            'objetivo': subtarefa.objetivo
        }

        return render(request, 'objetivos/editar_subtarefa.html', context)

    def post(self, request, subtarefa_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para editar subtarefas.")
            return redirect('logar')

        subtarefa = get_object_or_404(Subtarefa, id=subtarefa_id, objetivo__usuario_id=usuario_id)

        nome_subtarefa = request.POST.get('nome_subtarefa')
        descricao_subtarefa = request.POST.get('descricao_subtarefa')
        novo_status = request.POST.get('status')

        if not nome_subtarefa:
            messages.error(request, 'É necessário preencher o nome da subtarefa.')
            return redirect('editar_subtarefa', subtarefa_id=subtarefa_id)

        subtarefa.Nome = nome_subtarefa
        subtarefa.descrição = descricao_subtarefa
        subtarefa.Status = novo_status
        subtarefa.save()

        messages.success(request, f'Subtarefa "{nome_subtarefa}" atualizada com sucesso.')
        return redirect('visualizar_objetivos')