from django.db import models

# Usuário individual:
# cadastro: e-mail, senha, nome.

# objetivo:
# Nome, descrição, estar concluído

# Subtarefa:
# Nome, descrição, estar concluído

class Usuario(models.Model):
    Nome = models.CharField(max_length=100)
    E_mail = models.EmailField(unique=True)
    Senha = models.CharField(max_length=20)
    def __str__(self):
        return self.Nome

class Objetivo(models.Model):
    Nome = models.CharField(max_length=1000)
    Descrição = models.TextField()
    Estar_concluído = models.BooleanField(default=False)
    def __str__(self):
        return self.Nome


