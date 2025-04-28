from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Objetivo, Subtarefa,Grupos
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
        urgencia = request.POST.get('urgencia')  # Obter o valor de urgência

        # Validar o nome do objetivo
        if not nome_objetivo:
            messages.error(request, 'É necessário preencher o nome do objetivo.')
            return render(request, 'objetivos/criar_objetivo.html')

        # Verificar se já existe um objetivo com o mesmo nome para este usuário
        if Objetivo.objects.filter(nome=nome_objetivo, usuario_id=usuario_id).exists():
            messages.error(request, 'Você já tem uma tarefa com este nome. Por favor, escolha um nome diferente.')
            return render(request, 'objetivos/criar_objetivo.html', {
                'nome_objetivo': nome_objetivo,
                'descricao_objetivo': descricao_objetivo,
                'urgencia': urgencia
            })

        # Converter urgência para inteiro ou usar valor padrão
        try:
            urgencia_int = int(urgencia) if urgencia else 1
            # Garantir que está dentro dos limites (1-3)
            if urgencia_int < 1:
                urgencia_int = 1
            elif urgencia_int > 3:
                urgencia_int = 3
        except ValueError:
            urgencia_int = 1

        # Criar o objetivo associado ao usuário logado
        objetivo = Objetivo.objects.create(
            nome=nome_objetivo,
            descrição=descricao_objetivo,
            status='pendente',
            usuario_id=usuario_id,
            urgencia=urgencia_int
        )

        # Adicionando uma mensagem sobre a possibilidade de adicionar subtarefas
        messages.success(request, f'Objetivo "{nome_objetivo}" criado com sucesso! Deseja adicionar subtarefas?')
        
        # Redirecionar para visualização, mas incluir o ID do objetivo recém-criado
        return render(request, 'objetivos/objetivo_criado.html', {'objetivo': objetivo})


class VisualizarObjetivosView(View):
    def get(self, request):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para visualizar seus objetivos.")
            return redirect('logar')

        # Obter parâmetro de filtro da URL, se existir
        filtro_urgencia = request.GET.get('urgencia')
        
        # Iniciar com todos os objetivos do usuário
        objetivos_query = Objetivo.objects.filter(usuario_id=usuario_id)
        
        # Aplicar filtro de urgência, se especificado
        if filtro_urgencia:
            try:
                urgencia_valor = int(filtro_urgencia)
                objetivos_query = objetivos_query.filter(urgencia=urgencia_valor)
            except ValueError:
                # Se o valor não for um número válido, ignorar o filtro
                pass
        
        # Ordenar por urgência (decrescente)
        objetivos = objetivos_query.order_by('-urgencia')

        context = {
            'objetivos': objetivos,
            'filtro_atual': filtro_urgencia,  # Passar o filtro atual para o template
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

        nome_objetivo = objetivo.nome
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
        urgencia = request.POST.get('urgencia')  # Obter o valor de urgência

        # Validar o nome do objetivo
        if not nome_objetivo:
            messages.error(request, 'É necessário preencher o nome do objetivo.')
            return render(request, 'objetivos/editar_objetivo.html', {'objetivo': objetivo})

        # Verificar se já existe OUTRO objetivo com o mesmo nome para este usuário
        # Usamos exclude(id=objetivo_id) para não considerar o próprio objetivo na verificação
        if Objetivo.objects.filter(nome=nome_objetivo, usuario_id=usuario_id).exclude(id=objetivo_id).exists():
            messages.error(request, 'Você já tem uma tarefa com este nome. Por favor, escolha um nome diferente.')
            return render(request, 'objetivos/editar_objetivo.html', {
                'objetivo': objetivo,
                'nome_objetivo': nome_objetivo,
                'descricao_objetivo': descricao_objetivo,
                'urgencia': urgencia
            })

        # Converter urgência para inteiro ou manter o valor atual
        try:
            urgencia_int = int(urgencia) if urgencia else objetivo.urgencia
            # Garantir que está dentro dos limites (1-3)
            if urgencia_int < 1:
                urgencia_int = 1
            elif urgencia_int > 3:
                urgencia_int = 3
        except ValueError:
            urgencia_int = objetivo.urgencia

        objetivo.nome = nome_objetivo
        objetivo.descrição = descricao_objetivo
        objetivo.status = novo_status
        objetivo.urgencia = urgencia_int  # Atualizar o campo de urgência
        objetivo.save()

        messages.success(request, f'Objetivo "{nome_objetivo}" atualizado com sucesso!')
        return redirect('visualizar_objetivos')


class EditarSubtarefaView(View):
    def get(self, request, objetivo_id, subtarefa_id):
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)
        subtarefa = get_object_or_404(Subtarefa, id=subtarefa_id)

        if subtarefa.objetivo != objetivo:
            messages.error(request, "Subtarefa não pertence a esse objetivo.")
            return redirect('visualizar_objetivos')

        return render(request, 'objetivos/editar_subtarefa.html', {
            'objetivo': objetivo,
            'subtarefa': subtarefa
        })

    def post(self, request, objetivo_id, subtarefa_id):
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)
        subtarefa = get_object_or_404(Subtarefa, id=subtarefa_id)

        if subtarefa.objetivo != objetivo:
            messages.error(request, "Subtarefa não pertence a esse objetivo.")
            return redirect('visualizar_objetivos')

        nome_subtarefa = request.POST.get('nome_subtarefa')
        descricao_subtarefa = request.POST.get('descricao_subtarefa')
        status_subtarefa = request.POST.get('status_subtarefa')

        if not nome_subtarefa:
            messages.error(request, 'O nome da subtarefa é obrigatório.')
            return render(request, 'objetivos/editar_subtarefa.html', {
                'objetivo': objetivo,
                'subtarefa': subtarefa
            })

        # Verificar duplicidade de nome (excluindo a própria subtarefa)
        if Subtarefa.objects.filter(
            objetivo=objetivo,
            nome__iexact=nome_subtarefa  # case-insensitive
        ).exclude(id=subtarefa.id).exists():
            messages.error(request, f'Já existe outra subtarefa com o nome "{nome_subtarefa}" para este objetivo.')
            return render(request, 'objetivos/editar_subtarefa.html', {
                'objetivo': objetivo,
                'subtarefa': subtarefa
            })

        subtarefa.nome = nome_subtarefa
        subtarefa.descrição = descricao_subtarefa
        subtarefa.status = status_subtarefa
        subtarefa.save()

        messages.success(request, f'Subtarefa "{nome_subtarefa}" atualizada com sucesso.')
        return redirect('visualizar_objetivos')
        
class AdicionarSubtarefasView(View):
    def get(self, request, objetivo_id):
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para adicionar subtarefas.")
            return redirect('logar')

        objetivo = get_object_or_404(Objetivo, id=objetivo_id)

        if objetivo.usuario.id != usuario_id:
            messages.error(request, "Você não tem permissão para adicionar subtarefas a este objetivo.")
            return redirect('visualizar_objetivos')

        return render(request, 'objetivos/adicionar_subtarefas.html', {'objetivo': objetivo})

    def post(self, request, objetivo_id):
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para adicionar subtarefas.")
            return redirect('logar')

        objetivo = get_object_or_404(Objetivo, id=objetivo_id)

        if objetivo.usuario.id != usuario_id:
            messages.error(request, "Você não tem permissão para adicionar subtarefas a este objetivo.")
            return redirect('visualizar_objetivos')

        nome_subtarefa = request.POST.get('nome_subtarefa')
        descricao_subtarefa = request.POST.get('descricao_subtarefa')

        if not nome_subtarefa:
            messages.error(request, "O nome da subtarefa é obrigatório.")
            return redirect('adicionar_subtarefas', objetivo_id=objetivo.id)

        # Verificar se já existe uma subtarefa com o mesmo nome
        if Subtarefa.objects.filter(objetivo=objetivo, nome__iexact=nome_subtarefa).exists():
            messages.error(request, f'Já existe uma subtarefa com o nome "{nome_subtarefa}" para este objetivo.')
            return redirect('adicionar_subtarefas', objetivo_id=objetivo.id)

        Subtarefa.objects.create(
            nome=nome_subtarefa,
            descrição=descricao_subtarefa,
            status='pendente',
            objetivo=objetivo
        )

        messages.success(request, f'Subtarefa "{nome_subtarefa}" adicionada com sucesso ao objetivo "{objetivo.nome}".')
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
        nome_subtarefa = subtarefa.nome
        subtarefa.delete()

        messages.success(request, f'Subtarefa "{nome_subtarefa}" excluída com sucesso.')
        return redirect('visualizar_objetivos')

class VisualizarSubtarefasView(View):
    def get(self, request, objetivo_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para visualizar subtarefas.")
            return redirect('logar')

        # Buscar o objetivo pelo ID e verificar se pertence ao usuário logado
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)
        
        # Verificar se o objetivo pertence ao usuário logado
        if objetivo.usuario.id != usuario_id:
            messages.error(request, "Você não tem permissão para visualizar subtarefas deste objetivo.")
            return redirect('visualizar_objetivos')
        
        # Buscar todas as subtarefas do objetivo
        subtarefas = Subtarefa.objects.filter(objetivo=objetivo)
        
        context = {
            'objetivo_principal': objetivo,
            'subtarefas': subtarefas,
        }
        
        return render(request, 'objetivos/visualizar_subtarefas.html', context)
    
class Grupo(View):
    def get(self,request):
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para acessar grupos.")
            return redirect('logar')
        grupos=Grupos.objects.all()
        contexto={'grupos',grupos}
        return render(request,"objetivos/grupos.html",contexto)
    
    def post(self,request):
        nome_grupo_pesquisa=request.POST.get('nome_grupo_pesquisa')

        grupos_pesquisa=Grupos.objects.filter(Nome_grupo=nome_grupo_pesquisa)
        if not grupos_pesquisa:
            messages.error(request,"Esse grupo não existe")
            return render(request,"objetivos/grupos.html")
        contexto={'grupos_pesquisa',grupos_pesquisa}
        return render(request,'objetivos/grupos.html',contexto)
        #Terminar essa view. Ainda falta adicionar, quando a senha for correta em participantes/ botao_clicado=request.POST('botao_clicado')


    
class Meus_Grupos(View):
    def get(self,request):
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para os seus grupos.")
            return redirect('logar')
        meus_grupos=Grupos.objects.filter(Participantes=Usuario.username)
        contexto={'grupos_pesquisa',meus_grupos}
        return render(request,"objetivos/grupos.html",contexto)

    
class Criar_Grupo(View):
    def get(self,request):
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para criar grupos.")
            return redirect('logar')
        return render(request,"objetivos/criar_grupo.html")
    
    def post(self,request):

        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para criar grupos.")
            return redirect('logar')

        nome_grupo=request.POST.get('nome_grupo')
        qtd_membros_grupo=request.POST.get('qtd_membros_grupo')
        senha=request.POST.get('senha')
        
        if Objetivo.objects.filter(Nome_grupo=nome_grupo).exists():
            messages.error(request,'Esse grupo já existe')
            return render(request,"objetivos/criar_grupo.html")
        
        messages.success(request,"Grupo criado com sucesso")
        return('criar_grupo')