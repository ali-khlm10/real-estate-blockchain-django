from django.shortcuts import render
from django.views import View
from django.http import HttpRequest
from .models import blockModel
from utils.blockchain import real_estate_blockchain
# Create your views here.


class blockchainView(View):
    def get(self, request: HttpRequest):
        blocks: blockModel = blockModel.objects.all()
        blocks_of_blockchain = real_estate_blockchain.real_estate_chain
        context = {
            "blocks": blocks,
            "blocks_of_blockchain": blocks_of_blockchain,
        }
        return render(request, "blockchain_module/blockchain_page.html", context)
