from django.shortcuts import render
from django.views import View
from django.http import HttpRequest
from .models import blockModel
from utils.blockchain import real_estate_blockchain
import os
import json
import socket
# Create your views here.


class blockchainView(View):
    def get(self, request: HttpRequest):
        current_port = request.META['SERVER_PORT']
        if (int(current_port) >= 5000) and (int(current_port) < 6000):
            try:
                with open(f'utils/nodes_DB/{current_port}_DB.json', 'r') as json_file:
                    chain: list = json.load(json_file)["chain"]
                    json_file.close()
            except:
                chain = []

        else:
            chain: blockModel = blockModel.objects.all()
        # print(chain)
        context = {
            "blocks": chain,
        }
        return render(request, "blockchain_module/blockchain_page.html", context)


