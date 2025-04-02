from django.db import models

class Usuario(models.Model):
    Nome = models.CharField(max_length=100, unique=True)
    E_mail = models.EmailField(unique=True)
    Senha = models.CharField(max_length=20)

    def __str__(self):
        return self.Nome

class Objetivo(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('ativa', 'Ativa'),
        ('completa', 'Completa'),
    )
    
    Nome = models.CharField(max_length=1000)
    Descrição = models.TextField()
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='objetivos')

    def __str__(self):
        return self.Nome
    
    
class Subtarefa(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('ativa', 'Ativa'),
        ('completa', 'Completa'),
    )
    
    Nome = models.CharField(max_length=255)
    descrição = models.TextField(blank=True)
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE, related_name='subtarefas')

    def __str__(self):
        return self.Nome



