from django.urls import path
from objetivos.views import  CriarObjetivoView

urlpatterns = [
    path('',CriarObjetivoView.as_view(),name='criar_objetivo')
]

