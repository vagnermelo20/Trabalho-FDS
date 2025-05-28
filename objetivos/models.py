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
        return self.nome
    
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
        return self.nome

class Grupos(models.Model):
    Nome_grupo=models.CharField(max_length=1000,unique=True)
    Senha_grupo=models.CharField(max_length=100)
    Criador_grupo=models.ForeignKey(Usuario, on_delete=models.CASCADE)#Isso espera um valor que seja um objeto do tipo usuário
    def __str__(self):
        return self.Nome_grupo

class Participantes_grupos(models.Model):
    Grupos=models.CharField(max_length=1000)
    nome_participantes=models.CharField(max_length=100)

class Tarefas_grupos(models.Model):
    Nome=models.CharField(max_length=200)
    Descricao=models.CharField(max_length=1000)
    STATUS_ESCOLHAS = (
        ('pendente', 'Pendente'),
        ('ativa', 'Ativa'),
        ('completa', 'Completa'),
    )     
    Status=models.CharField(max_length=50, choices=STATUS_ESCOLHAS, default="pendente")
    Nome_participante=models.CharField(max_length=100)
    