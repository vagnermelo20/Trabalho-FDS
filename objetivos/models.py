from django.db import models

class Usuario(models.Model):
    Nome = models.CharField(max_length=100, unique=True)
    E_mail = models.EmailField(unique=True)
    Senha = models.CharField(max_length=20)

    def __str__(self):
        return self.Nome

class Objetivo(models.Model):
    Nome = models.CharField(max_length=1000)
    Descrição = models.TextField()
    Estar_concluído = models.BooleanField(default=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name= 'Objetivos')

    def __str__(self):
        return self.Nome
    
class Subtarefa(models.Model):
    Nome = models.CharField(max_length=255)
    descrição = models.TextField()
    estar_concluído = models.BooleanField(default=False)
    objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE, related_name='Subtarefas')

    def __str__(self):
        return self.Nome

