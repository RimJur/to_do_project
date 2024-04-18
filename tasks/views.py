from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class TaskListView(ListView):
    model = Task
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Task.objects.none()

        queryset = super().get_queryset().filter(user=self.request.user)
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
            return queryset
        else:
            return super().get_queryset().filter(
                user=self.request.user
            )


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task.html'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/create.html'
    fields = ['title', 'description', 'completed']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskEditView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/create.html'
    fields = ['title', 'description', 'completed']

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')