from django.shortcuts import render
from django.views import View
from django.http import HttpRequest
from .models import blockModel, transactionsModel, transactionStatusModel
from utils.blockchain import real_estate_blockchain
import os
import json
import socket
# Create your views here.


class blocksView(View):
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


class transactionsView(View):
    def get(self, request: HttpRequest):
        current_port = request.META['SERVER_PORT']
        if (int(current_port) >= 5000) and (int(current_port) < 6000):
            try:
                with open(f'utils/nodes_DB/{current_port}_DB_trxs.json', 'r') as json_file:
                    trxs: list = json.load(json_file)["transactions"]
                    trxs_status = []
                    for trx in trxs:
                        current_trx_status: transactionStatusModel = transactionStatusModel.objects.filter(
                            transaction_id=trx.get("transaction_id")).first()
                        if current_trx_status:
                            trxs_status.append(current_trx_status.status())
                        else:
                            trxs_status.append(False)
                    json_file.close()
            except:
                trxs = []
            # print(chain)
            context = {
                "zipped_list": zip(trxs, trxs_status),
                "current_port": int(current_port),
                "transactions_count": len(trxs),
            }
            return render(request, "blockchain_module/transactions_page.html", context)

        else:
            trxs: transactionsModel = transactionsModel.objects.all().order_by(
                "-transaction_timestamp")
            # print(chain)
            context = {
                "current_port": int(current_port),
                "trxs": trxs,
                "transactions_count": trxs.count(),

            }
            return render(request, "blockchain_module/transactions_page.html", context)
