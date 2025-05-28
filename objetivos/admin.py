from django.contrib import admin
from objetivos.models import  Objetivo, Subtarefa,Grupos,Tarefas_grupos,Participantes_grupos

admin.site.register(Objetivo) 

admin.site.register(Subtarefa)

admin.site.register(Grupos)
admin.site.register(Tarefas_grupos)
admin.site.register(Participantes_grupos)
