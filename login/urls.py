from django.urls import path
from login.views import CriarUsuarioView

urlpatterns = [
    path('', CriarUsuarioView.as_view(), name='criar_usuario'),
    
]

