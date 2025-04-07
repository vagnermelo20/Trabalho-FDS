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
        urgencia = request.POST.get('urgencia')  # Obter o valor de urgência

        # Validar o nome do objetivo
        if not nome_objetivo:
            messages.error(request, 'É necessário preencher o nome do objetivo.')
            return render(request, 'objetivos/criar_objetivo.html')

        # Verificar se já existe um objetivo com o mesmo nome para este usuário
        if Objetivo.objects.filter(Nome=nome_objetivo, usuario_id=usuario_id).exists():
            messages.error(request, 'Você já tem uma tarefa com este nome. Por favor, escolha um nome diferente.')
            return render(request, 'objetivos/criar_objetivo.html', {
                'nome_objetivo': nome_objetivo,
                'descricao_objetivo': descricao_objetivo,
                'urgencia': urgencia
            })

        # Converter urgência para inteiro ou usar valor padrão
        try:
            urgencia_int = int(urgencia) if urgencia else 1
            # Garantir que está dentro dos limites (1-5)
            if urgencia_int < 1:
                urgencia_int = 1
            elif urgencia_int > 3:
                urgencia_int = 3
        except ValueError:
            urgencia_int = 1

        # Criar o objetivo associado ao usuário logado
        Objetivo.objects.create(
            Nome=nome_objetivo,
            Descrição=descricao_objetivo,
            Status='pendente',
            usuario_id=usuario_id,
            urgencia=urgencia_int  # Adicionar o campo de urgência
        )

        return redirect('visualizar_objetivos')


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
        urgencia = request.POST.get('urgencia')  # Obter o valor de urgência

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
                'descricao_objetivo': descricao_objetivo,
                'urgencia': urgencia
            })

        # Converter urgência para inteiro ou manter o valor atual
        try:
            urgencia_int = int(urgencia) if urgencia else objetivo.urgencia
            # Garantir que está dentro dos limites (1-5)
            if urgencia_int < 1:
                urgencia_int = 1
            elif urgencia_int > 3:
                urgencia_int = 3
        except ValueError:
            urgencia_int = objetivo.urgencia

        objetivo.Nome = nome_objetivo
        objetivo.Descrição = descricao_objetivo
        objetivo.Status = novo_status
        objetivo.urgencia = urgencia_int  # Atualizar o campo de urgência
        objetivo.save()

        return redirect('visualizar_objetivos')