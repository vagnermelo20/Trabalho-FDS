from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, Objetivo, Todo
from objetivos.models import Objetivo, Subtarefa
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.views import View

# Create your views here.

class TaskList(ListView):
    model = Task
    fields = '__all__'
    context_object_name = 'tasks'
    

class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskUpdate(UpdateView):
    model = Task
    fields = ['number']
    success_url = reverse_lazy('tasks')

class TaskCreate(CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')