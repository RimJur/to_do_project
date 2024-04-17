from django.contrib import admin
from django.urls import path
from .views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskEditView,
    TaskDeleteView
)

urlpatterns = [
    path('', TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task'),
    path('task/create/', TaskCreateView.as_view(), name='create'),
    path('task/edit/<int:pk>/', TaskEditView.as_view(), name='edit'),
    path('task/delete/<int:pk>/', TaskDeleteView.as_view(), name='delete')
]
