from .views import SignUpView, CustomLoginView
from django.urls import path

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
]