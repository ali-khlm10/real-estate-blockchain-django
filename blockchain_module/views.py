from django.shortcuts import render
from django.views import View
from django.http import HttpRequest
from .models import blockModel, transactionsModel, transactionStatusModel, merkelTreeHashesModel
from utils.blockchain import real_estate_blockchain
import json
from account_module.models import userModel
from token_module.models import propertyTokenModel
from node_module.models import nodeModel
from token_module.models import smartContractModel
import hashlib
from django.views.decorators.csrf import csrf_exempt

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

            context = {
                "blocks": reversed(chain),
                "chain_length": len(chain),
            }
            return render(request, "blockchain_module/blockchain_page.html", context)

        else:
            chain: blockModel = blockModel.objects.all().order_by("-block_number")
        # print(chain)
            context = {
                "blocks": chain,
                "chain_length": len(chain),
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
                trxs_status = []
            context = {
                "zipped_list": zip(reversed(trxs), reversed(trxs_status)),
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


# ////////////////////////////////////////////////////////////////////


class blockView(View):
    def get(self, request: HttpRequest, block_number: int):
        block: blockModel = blockModel.objects.filter(
            block_number__iexact=block_number).first()
        print(block.block_hash)
        context = {
            "current_block": block,
        }
        return render(request, "blockchain_module/block_detailes.html", context)


class trxView(View):
    def get(self, request: HttpRequest, trx_hash: str):
        trx: transactionsModel = transactionsModel.objects.filter(
            transaction_hash__iexact=trx_hash).first()
        print(trx.transaction_fee)
        context = {
            "current_trx": trx,
        }
        return render(request, "blockchain_module/trx_detailes.html", context)


# ///////////////////////////////////////////////

class searchInformationView(View):
    def get(self, request: HttpRequest):
        context = {}
        return render(request, "blockchain_module/search_page.html", context)


class searchUserInformationView(View):
    def get(self, request: HttpRequest):
        user_address: str = request.GET.get("user_input")
        current_user: userModel = userModel.objects.filter(
            wallet__wallet_address__iexact=user_address).first()
        if current_user:
            trxs: transactionsModel = transactionsModel.objects.filter(
                transaction_from_address__iexact=current_user.wallet.wallet_address).all().order_by("-transaction_timestamp")
            last_trx = trxs.first()
            first_trx = trxs.last()
            tokens: propertyTokenModel = propertyTokenModel.objects.filter(
                property_owner_address__iexact=current_user.wallet.wallet_address)
            context = {
                "status": True,
                "current_user": current_user,
                "trxs": trxs,
                "first_trx": first_trx,
                "last_trx": last_trx,
                "tokens": tokens,
            }

        else:
            context = {
                "status": False,

            }
        return render(request, "blockchain_module/user_information_page.html", context)


class searchTokenInformationView(View):
    def get(self, request: HttpRequest):
        current_token_id: str = request.GET.get("token_input")
        token: propertyTokenModel = propertyTokenModel.objects.filter(
            token_id__iexact=current_token_id).first()
        if token:
            final_trxs = []
            property_transfers = []

            all_trxs: transactionsModel = transactionsModel.objects.all().order_by(
                "-transaction_timestamp")

            for trx in all_trxs:
                trx: transactionsModel
                if trx.transaction_type == "tokenization" or trx.transaction_type == "buy_request" or trx.transaction_type == "buy_operation":
                    if trx.transaction_data == current_token_id:
                        final_trxs.append(trx)

                else:
                    if trx.transaction_data is not None:
                        trx_data: dict = json.loads(trx.transaction_data)
                        if trx_data.get("token_id") == current_token_id:
                            final_trxs.append(trx)
                        if trx.transaction_type == "sell_operation" and trx_data.get("token_id") == current_token_id:
                            property_transfers.append(trx)

            # print(property_transfers)
            context = {
                "status": True,
                "token": token,
                "trxs": final_trxs,
                "property_transfers": None if len(property_transfers) == 0 else reversed(property_transfers),
            }
        else:
            context = {
                "status": False,
            }
        return render(request, "blockchain_module/token_information_page.html", context)


class searchNodeInformationView(View):
    def get(self, request: HttpRequest):
        node_address: str = request.GET.get("node_input")
        current_node: nodeModel = nodeModel.objects.filter(
            node_address__iexact=node_address).first()
        if current_node:
            context = {
                "status": True,
                "current_node": current_node,
            }
        else:
            context = {
                "status": False,
            }
        return render(request, "blockchain_module/node_information_page.html", context)


class searchSmartContractInformationView(View):
    def get(self, request: HttpRequest):
        smart_contract_address: str = request.GET.get("smart_contract_input")
        current_smart_contract: smartContractModel = smartContractModel.objects.filter(
            contract_address__iexact=smart_contract_address).first()
        if current_smart_contract:
            context = {
                "status": True,
                "current_smart_contract": current_smart_contract,
            }
        else:
            context = {
                "status": False,
            }
        return render(request, "blockchain_module/smart_contract_information_page.html", context)


# ////////////////////////////////////////////////


class verifyTransactionView(View):
    def get(self, request: HttpRequest):
        trx_hash: str = request.GET.get("trx_input")
        current_trx: transactionsModel = transactionsModel.objects.filter(
            transaction_hash__iexact=trx_hash).first()
        if current_trx:
            block_merkel_tree_hash = current_trx.transaction_block.block_merkel_tree_root_hash
            current_hash = current_trx.transaction_hash
            while current_hash:
                merkel_tree_hash_left: merkelTreeHashesModel = merkelTreeHashesModel.objects.filter(
                    current_hash__iexact=current_hash).first()

                merkel_tree_hash_right: merkelTreeHashesModel = merkelTreeHashesModel.objects.filter(
                    combined_hash__iexact=current_hash).first()

                if merkel_tree_hash_left:
                    if merkel_tree_hash_left.combined_hash is not None:
                        merged_hash: str = current_hash + merkel_tree_hash_left.combined_hash
                        new_hash = hashlib.sha512(
                            merged_hash.encode('utf-8')).hexdigest()
                        current_hash = "0x" + new_hash[:64]
                        root_hash = "0x" + new_hash[:64]
                    else:
                        current_hash = None

                elif merkel_tree_hash_right:
                    if merkel_tree_hash_right.current_hash is not None:
                        merged_hash: str = merkel_tree_hash_right.current_hash + current_hash
                        new_hash = hashlib.sha512(
                            merged_hash.encode('utf-8')).hexdigest()
                        current_hash = "0x" + new_hash[:64]
                        root_hash = "0x" + new_hash[:64]
                    else:
                        current_hash = None

                else:
                    current_hash = None

            if root_hash == block_merkel_tree_hash:
                message = "تراکنش مورد نظر معتبر می باشد و با توجه به تاییدیه درخت مرکل هیچ تغییر یا جابه جایی در اطلاعات این تراکنش صورت نگرفته است."
                context = {
                    "status": True,
                    "current_node": current_trx,
                    "message": message,
                    "valid": True,
                }
            else:
                message = "تراکنش نامعتبر است."
                context = {
                    "status": True,
                    "current_node": current_trx,
                    "message": message,
                    "valid": False,

                }

        else:
            context = {
                "status": False,
            }
        return render(request, "blockchain_module/verify_trx_page.html", context)


class verifyBlockchainView(View):
    def get(self, request: HttpRequest):
        current_chain = real_estate_blockchain.real_estate_chain
        result: bool = real_estate_blockchain.is_chain_valid(
            chain=current_chain)

        if result:
            message = "زنجیره بلوکی معتبر می باشد و هیچ گونه تغییری در بلوک ها وجود ندارد."
            context = {
                "message": message,
                "valid": True,
            }
        else:
            message = "زنجیره بلوکی نامعتبر است."
            context = {
                "message": message,
                "valid": False,

            }
        return render(request, "blockchain_module/verify_blockchain_page.html", context)
