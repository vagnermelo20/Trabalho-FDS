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
        
        return render(request, 'objetivos/criar_objetivo.html')
    
    def post(self, request):
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para criar objetivos.")
            return redirect('logar')
        
        # Buscar o usuário pelo ID na sessão
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
            del request.session['usuario_id']
            return redirect('logar')
        
        nome_objetivo = request.POST.get('nome_objetivo')
        descricao_objetivo = request.POST.get('descricao_objetivo')

        if not nome_objetivo:
            messages.error(request, 'É necessário preencher o nome do objetivo.')
            return render(request, 'objetivos/criar_objetivo.html')

        # Criar o objetivo
        objetivo = Objetivo.objects.create(
            Nome=nome_objetivo,
            Descrição=descricao_objetivo,
            Status='pendente',
            usuario=usuario
        )

        messages.success(request, f'Objetivo "{nome_objetivo}" foi criado com sucesso!')
        
        # Redireciona para a página de visualização de objetivos com a opção de adicionar subtarefa
        return render(request, 'objetivos/objetivo_criado.html', {'objetivo': objetivo})



class VisualizarObjetivosView(View):
    def get(self, request):
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para visualizar seus objetivos.")
            return redirect('logar')

        usuario = get_object_or_404(Usuario, id=usuario_id)
        
        # Usando 'subtarefas' como related_name
        objetivos = Objetivo.objects.filter(usuario=usuario).prefetch_related('subtarefas')

        context = {
            'objetivos': objetivos,
            'usuario': usuario
        }

        return render(request, 'objetivos/visualizar_objetivos.html', context)

class DeletarObjetivoView(View):
    def post(self, request, objetivo_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para excluir objetivos.")
            return redirect('logar')
            
        # Buscar o objetivo e verificar se pertence ao usuário
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)
        
        if objetivo.usuario.id != usuario_id:
            messages.error(request, "Você não tem permissão para excluir este objetivo.")
            return redirect('visualizar_objetivos')
        
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
            
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)
        
        if objetivo.usuario.id != usuario_id:
            messages.error(request, "Você não tem permissão para editar este objetivo.")
            return redirect('visualizar_objetivos')
            
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
            
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)
        
        if objetivo.usuario.id != usuario_id:
            messages.error(request, "Você não tem permissão para editar este objetivo.")
            return redirect('visualizar_objetivos')
            
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
    def get(self, request, objetivo_id, subtarefa_id):
        # Buscar o objetivo e a subtarefa pelo ID
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)
        subtarefa = get_object_or_404(Subtarefa, id=subtarefa_id)

        # Verificar se a subtarefa pertence ao objetivo
        if subtarefa.objetivo != objetivo:
            messages.error(request, "Subtarefa não pertence a esse objetivo.")
            return redirect('visualizar_objetivos')

        # Passar a subtarefa e o objetivo para o template
        return render(request, 'objetivos/editar_subtarefa.html', {
            'objetivo': objetivo,
            'subtarefa': subtarefa
        })

    def post(self, request, objetivo_id, subtarefa_id):
        # Buscar o objetivo e a subtarefa pelo ID
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)
        subtarefa = get_object_or_404(Subtarefa, id=subtarefa_id)

        # Verificar se a subtarefa pertence ao objetivo
        if subtarefa.objetivo != objetivo:
            messages.error(request, "Subtarefa não pertence a esse objetivo.")
            return redirect('visualizar_objetivos')

        # Obter os dados do formulário
        nome_subtarefa = request.POST.get('nome_subtarefa')
        descricao_subtarefa = request.POST.get('descricao_subtarefa')
        status_subtarefa = request.POST.get('status_subtarefa')

        # Validar os dados
        if not nome_subtarefa:
            messages.error(request, 'O nome da subtarefa é obrigatório.')
            return render(request, 'objetivos/editar_subtarefa.html', {
                'objetivo': objetivo,
                'subtarefa': subtarefa
            })

        # Atualizar a subtarefa
        subtarefa.Nome = nome_subtarefa
        subtarefa.descrição = descricao_subtarefa
        subtarefa.Status = status_subtarefa
        subtarefa.save()

        messages.success(request, f'Subtarefa "{nome_subtarefa}" atualizada com sucesso.')
        return redirect('visualizar_objetivos')

class AdicionarSubtarefasView(View):
    def get(self, request, objetivo_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para adicionar subtarefas.")
            return redirect('logar')

        # Buscar o objetivo
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)

        # Verificar se o objetivo pertence ao usuário
        if objetivo.usuario.id != usuario_id:
            messages.error(request, "Você não tem permissão para adicionar subtarefas a este objetivo.")
            return redirect('visualizar_objetivos')

        return render(request, 'objetivos/adicionar_subtarefas.html', {'objetivo': objetivo})

    def post(self, request, objetivo_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para adicionar subtarefas.")
            return redirect('logar')

        # Buscar o objetivo
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)

        # Verificar se o objetivo pertence ao usuário
        if objetivo.usuario.id != usuario_id:
            messages.error(request, "Você não tem permissão para adicionar subtarefas a este objetivo.")
            return redirect('visualizar_objetivos')

        # Processar o formulário
        nome_subtarefa = request.POST.get('nome_subtarefa')
        descricao_subtarefa = request.POST.get('descricao_subtarefa')

        if not nome_subtarefa:
            messages.error(request, "O nome da subtarefa é obrigatório.")
            return redirect('adicionar_subtarefas', objetivo_id=objetivo.id)

        # Criar a subtarefa
        Subtarefa.objects.create(
            Nome=nome_subtarefa,
            descrição=descricao_subtarefa,
            Status='pendente',
            objetivo=objetivo
        )

        messages.success(request, f'Subtarefa "{nome_subtarefa}" adicionada com sucesso ao objetivo "{objetivo.Nome}".')
        return redirect('visualizar_objetivos')

class DeletarSubtarefaView(View):
    def post(self, request, objetivo_id, subtarefa_id):
        # Buscar o objetivo e a subtarefa pelo ID
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)
        subtarefa = get_object_or_404(Subtarefa, id=subtarefa_id)

        # Verificar se a subtarefa pertence ao objetivo
        if subtarefa.objetivo != objetivo:
            messages.error(request, "Subtarefa não pertence a esse objetivo.")
            return redirect('visualizar_objetivos')

        # Deletar a subtarefa
        subtarefa.delete()

        messages.success(request, f'Subtarefa "{subtarefa.Nome}" excluída com sucesso.')
        return redirect('visualizar_objetivos')