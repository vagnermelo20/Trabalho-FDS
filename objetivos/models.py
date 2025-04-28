from django.db import models
from login.models import Usuario


class Objetivo(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('ativa', 'Ativa'),
        ('completa', 'Completa'),
    )     
    Nome = models.CharField(max_length=1000)
    Descrição = models.TextField()
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    usuario = models.ForeignKey('login.Usuario', on_delete=models.CASCADE,related_name= 'Objetivos')

    def __str__(self):
        return self.Nome
    
class Subtarefa(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em andamento', 'Em andamento'),
        ('concluída', 'Concluída'),
    ]
    
    Nome = models.CharField(max_length=200)
    descrição = models.TextField()
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE, related_name='subtarefas')  # AQUI

    def __str__(self):
        return self.Nome


