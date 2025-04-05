from django.urls import path
from objetivos.views import  CriarObjetivoView,VisualizarObjetivosView

urlpatterns = [
    path('',VisualizarObjetivosView.as_view(),name='visualizar_objetivo'),
    path('criar_objetivo/',CriarObjetivoView.as_view(),name='visualizar_objetivo')
]

