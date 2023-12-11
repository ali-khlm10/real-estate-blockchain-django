import json
from django.shortcuts import render
from django.http import HttpRequest,JsonResponse
from django.views.decorators.csrf import csrf_exempt



# Create your views here.



@csrf_exempt
def createPropertySignature(request: HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        return JsonResponse({"true": True})