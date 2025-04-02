from django.urls import path
from app.views import CriarUsuarioView, CriarObjetivoView

urlpatterns = [
    path('criar-usuario/', CriarUsuarioView.as_view(), name='criar_usuario'),
    path('criar-objetivo/', CriarObjetivoView.as_view(), name='criar_objetivo'),
]

