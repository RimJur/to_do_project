from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import AccessMixin

# Create your views here.

class RedirectIfAuthenticatedMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)

class SignUpView(RedirectIfAuthenticatedMixin, CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class CustomLoginView(RedirectIfAuthenticatedMixin, LoginView):
    template_name = 'registration/login.html'