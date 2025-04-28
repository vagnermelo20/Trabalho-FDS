from django.db import models
from login.models import Usuario
from django.core.validators import MaxValueValidator, MinValueValidator

class Objetivo(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('ativa', 'Ativa'),
        ('completa', 'Completa'),
    )     
    nome = models.CharField(max_length=1000)
    descrição = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    usuario = models.ForeignKey('login.Usuario', on_delete=models.CASCADE,related_name= 'Objetivos')
    urgencia = models.IntegerField(null=True, blank=True, default=0,
        validators=[
            MaxValueValidator(3),  
            MinValueValidator(1),     
        ]
    )

    def __str__(self):
        return self.Nome
    
class Subtarefa(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em andamento', 'Em andamento'),
        ('concluída', 'Concluída'),
    ]
    
    nome = models.CharField(max_length=200)
    descrição = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE, related_name='subtarefas')  # AQUI

    def __str__(self):
        return self.Nome


