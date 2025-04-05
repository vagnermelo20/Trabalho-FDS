from django.urls import path
from objetivos.views import CriarObjetivoView, DeletarObjetivoView, EditarObjetivoView, VisualizarObjetivosView

urlpatterns = [
    path('', VisualizarObjetivosView.as_view(), name='visualizar_objetivos'),
    path('criar_objetivo/', CriarObjetivoView.as_view(), name='criar_objetivo'),  # Corrigido o nome da URL
    path('editar_objetivo/<int:objetivo_id>/', EditarObjetivoView.as_view(), name='editar_objetivo'),
    path('deletar_objetivo/<int:objetivo_id>/', DeletarObjetivoView.as_view(), name='deletar_objetivo'),
]

