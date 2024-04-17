from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from django.urls import reverse_lazy

# Create your views here.

class TaskListView(ListView):
    model = Task

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task.html'

class TaskCreateView(CreateView):
    model = Task
    template_name = 'tasks/create.html'
    fields = ['user', 'title', 'description', 'completed']

class TaskEditView(UpdateView):
    model = Task
    template_name = 'tasks/create.html'
    fields = ['title', 'description', 'completed']

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')