
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
            return redirect('login')
        
        lista_objetivos=Objetivo.objects.all()
        contexto={'objetivos':lista_objetivos}
        return render(request,'objetivos/criar_objetivo.html',contexto)
        
    
    def post(self, request):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para criar objetivos.")
            return redirect('login')
            
        # Buscar o usuário pelo ID na sessão
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
            # Limpar a sessão se o usuário não existir mais
            del request.session['usuario_id']
            return redirect('login')
        
        nome_objetivo = request.POST.get('nome_objetivo')
        descricao_objetivo = request.POST.get('descricao_objetivo')
        subtarefas_nomes = request.POST.getlist('subtarefa_nome')
        subtarefas_descricoes = request.POST.getlist('subtarefa_descricao')

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
        return redirect('visualizar_objetivos')  # Redirecionar para a visualização após criação


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
            return redirect('visualizar_objetivos')
        
        # Guardar o nome para mensagem de confirmação
        nome_objetivo = objetivo.Nome
        
        # Excluir o objetivo (isso também excluirá as subtarefas devido à relação CASCADE)
        objetivo.delete()
        
        messages.success(request, f'Objetivo "{nome_objetivo}" foi excluído com sucesso.')
        
        # Redirecionar para a página de visualização mantendo o filtro
        filtro = request.POST.get('filtro_atual', 'todos')
        return redirect(f'/objetivos/?filtro={filtro}')