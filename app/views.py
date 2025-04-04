from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Usuario, Objetivo, Subtarefa
from django.http import HttpResponse

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
        return redirect('login')  # Redirecionar para página de login após criação

class CriarObjetivoView(View):
    def get(self, request):
        # Verificar se o usuário está logado
        if 'usuario_id' not in request.session:
            messages.error(request, "Você precisa estar logado para criar objetivos.")
            return redirect('login')
        return render(request, 'criar_objetivo.html')
    
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

# Nova view para alterar o status de um objetivo
class AlterarStatusObjetivoView(View):
    def post(self, request, objetivo_id):
        # Verificar se o usuário está logado
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Você precisa estar logado para alterar objetivos.")
            return redirect('login')
            
        # Buscar o objetivo e verificar se pertence ao usuário
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)
        
        # Verificar se o objetivo pertence ao usuário logado
        if objetivo.usuario.id != usuario_id:
            messages.error(request, "Você não tem permissão para alterar este objetivo.")
            return redirect('visualizar_objetivos')
            
        # Obter o novo status do formulário
        novo_status = request.POST.get('status')
        
        # Validar o status
        if novo_status not in ['pendente', 'ativa', 'completa']:
            messages.error(request, "Status inválido.")
            return redirect('visualizar_objetivos')
            
        # Atualizar o status
        objetivo.Status = novo_status
        objetivo.save()
        
        messages.success(request, f'Status do objetivo "{objetivo.Nome}" alterado para "{objetivo.get_Status_display()}".')
        
        # Redirecionar para a página de visualização mantendo o filtro
        filtro = request.POST.get('filtro_atual', 'todos')
        return redirect(f'/objetivos/?filtro={filtro}')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not email or not senha:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('login')

        try:
            usuario = Usuario.objects.get(E_mail=email)
            if usuario.Senha == senha:
                request.session['usuario_id'] = usuario.id
                messages.success(request, f'Bem-vindo(a), {usuario.Nome}!')
                return redirect('visualizar_objetivos')  # Redireciona para visualização após login
            else:
                messages.error(request, 'Senha incorreta.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')

        return redirect('login')