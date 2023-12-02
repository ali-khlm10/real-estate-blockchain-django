from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginView.as_view(), name='login-page'),
    path("register/", views.registerView.as_view(), name='register-page'),
]
