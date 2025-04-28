from django.urls import path
from login.views import CriarUsuarioView,LoginView

urlpatterns = [
    path('', LoginView.as_view(), name='logar'),
    path('criar_usuario/',CriarUsuarioView.as_view(),name='criar_usuario'),
    
]

