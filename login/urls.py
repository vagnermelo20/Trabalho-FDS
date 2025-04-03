from django.urls import path
from login.views import CriarUsuarioView, CriarObjetivoView

urlpatterns = [
    
    path('', CriarUsuarioView.as_view(), name='criar_usuario'),
    path('objetivo/criar_objetivo/', CriarObjetivoView.as_view(), name='criar_objetivo'),
]

