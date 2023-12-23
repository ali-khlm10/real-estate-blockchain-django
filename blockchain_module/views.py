from django.shortcuts import render
from django.views import View
from django.http import HttpRequest
# Create your views here.


class blockchainView(View):
    def get(self, request: HttpRequest):
        context = {}
        return render(request, "blockchain_module/blockchain_page.html", context)
