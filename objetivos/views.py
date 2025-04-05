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

        Objetivo.objects.create(
            Nome=nome_objetivo,
            Descrição=descricao_objetivo,
            Status='pendente',
            usuario=usuario
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
            
        # Buscar o usuário pelo ID na sessão
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
            del request.session['usuario_id']
            return redirect('logar')
        
        # Buscar todos os objetivos do usuário
        objetivos = Objetivo.objects.filter(usuario=usuario)
        
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
    def get(self, request, subtarefa_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para editar subtarefas.")
            return redirect('logar')
            
        subtarefa = get_object_or_404(Subtarefa, id=subtarefa_id)
        
        if subtarefa.objetivo.usuario.id != usuario_id:
            messages.error(request, "Você não tem permissão para editar esta subtarefa.")
            return redirect('visualizar_objetivos')
            
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
            
        subtarefa = get_object_or_404(Subtarefa, id=subtarefa_id)
        
        if subtarefa.objetivo.usuario.id != usuario_id:
            messages.error(request, "Você não tem permissão para editar esta subtarefa.")
            return redirect('visualizar_objetivos')
            
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