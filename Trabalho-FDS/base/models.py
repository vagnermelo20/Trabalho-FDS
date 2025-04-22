from django.db import models
from django.contrib.auth.models import User
from objetivos.models import Objetivo
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank = True)
    title = models.CharField(max_length=200)
    description = models.TextField( null=True, blank = True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    number = models.IntegerField(null=True, blank=True, default=0, help_text="Enter a number between 1 and 10",
        validators=[
            MaxValueValidator(10),  
            MinValueValidator(1),     
        ]
    )
        

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']

class Todo(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank = True)
    title = models.CharField(max_length=200)
    description = models.TextField( null=True, blank = True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    number = models.IntegerField(null=True, blank=True, default=0, help_text="Enter a number between 1 and 10",
        validators=[
            MaxValueValidator(10),  
            MinValueValidator(1),     
        ]
    )
        

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']

