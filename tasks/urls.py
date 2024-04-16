from django.contrib import admin
from django.urls import path
from .views import (
    TaskListView,

)

urlpatterns = [
    path('', TaskListView.as_view(), name='index'),
]
