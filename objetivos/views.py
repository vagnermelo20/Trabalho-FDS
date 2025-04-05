from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import  Objetivo, Subtarefa
from login.models import Usuario




class CriarObjetivoView(View):
    def get(self, request):
        # Verificar se o usuário está logado
        if 'usuario_id' not in request.session:
            messages.error(request, "Você precisa estar logado para criar objetivos.")
            return redirect('logar')
        
        lista_objetivos=Usuario.objects.all() 
        contexto={'objetivo': lista_objetivos}  
        return render(request,'objetivos/visualizar_objetivos.html',contexto)
        
    
    def post(self, request):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para criar objetivos.")
            return render(request,'login/logar.html')
            
        # Buscar o usuário pelo ID na sessão
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
            # Limpar a sessão se o usuário não existir mais
            del request.session['usuario_id']
            return render(request,'login/logar.html')
        
        nome_objetivo = request.POST.get('nome_objetivo')
        descricao_objetivo = request.POST.get('descricao_objetivo')

        if not nome_objetivo:
            messages.error(request, 'É necessário preencher o nome do objetivo.')
            return render(request, 'objetivos/criar_objetivo.html')

        objetivo = Objetivo.objects.create(
            Nome=nome_objetivo,
            Descrição=descricao_objetivo,
            Status='pendente',  # Estado inicial é "pendente"
            usuario=usuario
        )

        messages.success(
            request,
            f'Objetivo "{nome_objetivo}" foi criado com sucesso!'
        )
        # Redirecionar para a visualização após criação


class VisualizarObjetivosView(View):
    def get(self, request):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para visualizar seus objetivos.")
            return redirect('login')
            
        # Buscar o usuário pelo ID na sessão
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
            # Limpar a sessão se o usuário não existir mais
            del request.session['usuario_id']
            return redirect('login')
            
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
            'filtro_atual': filtro,
            'usuario': usuario  # Passamos o usuário para o template
        }
        
        return render(request, 'visualizar_objetivos.html', context)


class DeletarObjetivoView(View):
    def post(self, request, objetivo_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para excluir objetivos.")
            return redirect('login')
            
        # Buscar o objetivo e verificar se pertence ao usuário
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)
        
        # Verificar se o objetivo pertence ao usuário logado
        if objetivo.usuario.id != usuario_id:
            messages.error(request, "Você não tem permissão para excluir este objetivo.")
            return render(request,'objetivos/visualizar_objetivos.html')
        
        # Guardar o nome para mensagem de confirmação
        nome_objetivo = objetivo.Nome
        
        # Excluir o objetivo (isso também excluirá as subtarefas devido à relação CASCADE)
        objetivo.delete()
        
        messages.success(request, f'Objetivo "{nome_objetivo}" foi excluído com sucesso.')
        
       
        
 


class EditarObjetivoView(View):
    def get(self, request, objetivo_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para editar objetivos.")
            return redirect('login')
            
        # Buscar o objetivo e verificar se pertence ao usuário
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)
        
        # Verificar se o objetivo pertence ao usuário logado
        if objetivo.usuario.id != usuario_id:
            messages.error(request, "Você não tem permissão para editar este objetivo.")
            return render(request,'objetivos/visualizar_objetivos.html')
            
        context = {
            'objetivo': objetivo,
        }
        
        return render(request, 'objetivos/editar_objetivo.html', context)
    
    def post(self, request, objetivo_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para editar objetivos.")
            return redirect('login')
            
        # Buscar o objetivo e verificar se pertence ao usuário
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)
        
        # Verificar se o objetivo pertence ao usuário logado
        if objetivo.usuario.id != usuario_id:
            messages.error(request, "Você não tem permissão para editar este objetivo.")
            return render(request,'objetivos/visualizar_objetivos.html')
            
        # Obter os dados do formulário
        nome_objetivo = request.POST.get('nome_objetivo')
        descricao_objetivo = request.POST.get('descricao_objetivo')
        novo_status = request.POST.get('status')
        
        # Validar os dados
        if not nome_objetivo:
            messages.error(request, 'É necessário preencher o nome do objetivo.')
            return redirect('editar_objetivo', objetivo_id=objetivo_id)
            
        if novo_status not in ['pendente', 'ativa', 'completa']:
            messages.error(request, "Status inválido.")
            return redirect('editar_objetivo', objetivo_id=objetivo_id)
            
        # Atualizar os dados do objetivo
        objetivo.Nome = nome_objetivo
        objetivo.Descrição = descricao_objetivo
        objetivo.Status = novo_status
        objetivo.save()
        
        messages.success(request, f'Objetivo "{nome_objetivo}" atualizado com sucesso.')
        
        # Redirecionar para a página de visualização mantendo o filtro de pendentes, ativas, completas ou todas
        filtro = request.POST.get('filtro_atual', 'todos')
        return redirect(f'/objetivos/?filtro={filtro}')

class EditarSubtarefaView(View):
    def get(self, request, subtarefa_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para editar subtarefas.")
            return redirect('login')
            
        # Buscar a subtarefa
        subtarefa = get_object_or_404(Subtarefa, id=subtarefa_id)
        
        # Verificar se o objetivo da subtarefa pertence ao usuário logado
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
            return redirect('login')
            
        # Buscar a subtarefa
        subtarefa = get_object_or_404(Subtarefa, id=subtarefa_id)
        
        # Verificar se o objetivo da subtarefa pertence ao usuário logado
        if subtarefa.objetivo.usuario.id != usuario_id:
            messages.error(request, "Você não tem permissão para editar esta subtarefa.")
            return redirect('visualizar_objetivos')
            
        # Obter os dados do formulário
        nome_subtarefa = request.POST.get('nome_subtarefa')
        descricao_subtarefa = request.POST.get('descricao_subtarefa')
        novo_status = request.POST.get('status')
        
        # Validar os dados
        if not nome_subtarefa:
            messages.error(request, 'É necessário preencher o nome da subtarefa.')
            return redirect('editar_subtarefa', subtarefa_id=subtarefa_id)
            
        if novo_status not in ['pendente', 'ativa', 'completa']:
            messages.error(request, "Status inválido.")
            return redirect('editar_subtarefa', subtarefa_id=subtarefa_id)
            
        # Atualizar os dados da subtarefa
        subtarefa.Nome = nome_subtarefa
        subtarefa.descrição = descricao_subtarefa
        subtarefa.Status = novo_status
        subtarefa.save()
        
        messages.success(request, f'Subtarefa "{nome_subtarefa}" atualizada com sucesso.')
        
        # Redirecionar para a página de visualização do objetivo pai
        objetivo_id = subtarefa.objetivo.id
        return redirect(f'/objetivos/?objetivo_id={objetivo_id}')