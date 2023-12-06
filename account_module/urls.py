from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registerView.as_view(), name='register-page'),
    path("login/", views.loginView.as_view(), name='login-page'),
    path("logout/", views.logoutView.as_view(), name='logout-page'),
]
