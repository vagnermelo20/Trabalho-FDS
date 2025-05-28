from django.urls import path
from objetivos.views import (CriarObjetivoView, DeletarObjetivoView, EditarObjetivoView, 
                            VisualizarObjetivosView, AdicionarSubtarefasView, 
                            EditarSubtarefaView, DeletarSubtarefaView, 
                            VisualizarSubtarefasView,Meus_Grupos,Criar_Grupo,Senha,VisualizarGrupos,CriarTarefaAdm,)
from . import views

urlpatterns = [
    path('', VisualizarObjetivosView.as_view(), name='visualizar_objetivos'),
    path('criar_objetivo/', CriarObjetivoView.as_view(), name='criar_objetivo'),  # Corrigido o nome da URL
    path('editar_objetivo/<int:objetivo_id>/', EditarObjetivoView.as_view(), name='editar_objetivo'),
    path('deletar_objetivo/<int:objetivo_id>/', DeletarObjetivoView.as_view(), name='deletar_objetivo'),
    path('objetivos/<int:objetivo_id>/subtarefas/', VisualizarSubtarefasView.as_view(), name='visualizar_subtarefas'),
    path('objetivos/<int:objetivo_id>/subtarefas/adicionar/', AdicionarSubtarefasView.as_view(), name='adicionar_subtarefas'),
    path('objetivos/<int:objetivo_id>/subtarefas/<int:subtarefa_id>/editar/', EditarSubtarefaView.as_view(), name='editar_subtarefa'),
    path('objetivos/<int:objetivo_id>/subtarefas/<int:subtarefa_id>/deletar/', DeletarSubtarefaView.as_view(), name='deletar_subtarefa'),
    path('meus_grupos/',Meus_Grupos.as_view(),name='meus_grupos'),
    path('criar_grupo/',Criar_Grupo.as_view(),name='criar_grupo'),
    path('visualizar_grupo/<str:grupo>/',VisualizarGrupos.as_view(),name='visualizar_grupos'),
    path('senha/',Senha.as_view(),name='senha'),
    path("criar_tarefa_adm/<str:grupo>/",CriarTarefaAdm.as_view(),name='criar_tarefa_adm')
]

