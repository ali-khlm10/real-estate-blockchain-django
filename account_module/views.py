from django.shortcuts import render
from django.views import View
from django.http import HttpRequest
from .forms import *
# Create your views here.


class registerView(View):
    def get(self, request: HttpRequest):
        registeration_form: registerForm = registerForm()
        context = {
            "registeration_form": registeration_form,
        }
        return render(request, "account_module/register_page.html", context)


class loginView(View):
    def get(self, request: HttpRequest):
        context = {}
        return render(request, "account_module/login_page.html", context)
