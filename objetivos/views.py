from django.shortcuts import render

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, Objetivo, Subtarefa



class CriarObjetivoView(View):
    def get(self, request):

        return render(request,'objetivos/criar_objetivo.html')

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
                    objetivo=objetivo
                )
                count += 1

        messages.success(
            request,
            f'Objetivo "{nome_objetivo}" foi criado com sucesso com {count} subtarefa(s).'
        )
        return redirect('criar_objetivo')