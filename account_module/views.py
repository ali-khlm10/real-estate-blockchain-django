from django.shortcuts import render
from django.views import View
from django.http import HttpRequest

# Create your views here.



class registerView(View):
    def get(self, request : HttpRequest):
        context = {}
        return render(request,"account_module/register_page.html",context)
    

class loginView(View):
    def get(self, request : HttpRequest):
        context = {}
        return render(request,"account_module/login_page.html",context)
    