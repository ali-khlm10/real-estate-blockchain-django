import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.create_and_verify_signature import create_signature, verify_signature
from utils.generate_pair_key import pem_to_private_key, pem_to_public_key
from utils.smart_contract import smart_contract_address
from property_module.models import propertyModel
from account_module.models import userModel
from django.views import View
from utils.create_and_verify_signature import verify_signature
from .models import propertyTokenModel
import hashlib
from utils.blockchain import real_estate_blockchain
from blockchain_module.models import transactionsModel

from node_module.models import nodeModel
from django.middleware import csrf
import requests

# Create your views here.


def create_token_id(token_information):
    token_information_str: str = json.dumps(token_information)
    hex_hash = hashlib.sha512(
        token_information_str.encode('utf-8')).hexdigest()
    int_hash = int(hex_hash, 16)

    return str(int_hash)[:80]


def create_token(data: dict):
    property_signature = data.get("signature")
    property_information: dict = data.get("property_information")
    property_id = property_information.get("property_id")
    current_property: propertyModel = propertyModel.objects.filter(
        id__exact=property_id).first()
    token_info: dict = current_property.property_detailes.detailes()
    token_info["property_creator_id"] = current_property.property_creator_id
    token_info["property_owner_address"] = current_property.property_owner_address
    token_info["property_signature"] = property_signature
    new_token_id = create_token_id(token_information=token_info)
    new_token: propertyTokenModel = propertyTokenModel.objects.create(
        property_of_token=current_property,
        property_owner_address=current_property.property_owner_address,
        token_id=new_token_id,
        token_information=json.dumps(token_info),
    )
    new_token.save()
    # current_property.token_generated = True
    # current_property.save()

    create_new_transaction: dict = real_estate_blockchain.add_transaction(
        transaction_info={
            "transaction_type": "tokenization",
            "data": data,
            "token_id": new_token.token_id,
            "transaction_fee": data.get("transaction_fee"),
        }
    )

    replace_transactions_result: bool = real_estate_blockchain.replace_transactions(
        trx=create_new_transaction.get("transaction"))

    if replace_transactions_result:
        if len(real_estate_blockchain.real_estate_transactions) != 0:
            miner_node: nodeModel = real_estate_blockchain.proof_of_stake()
            csrf_token = csrf.get_token(request=HttpRequest())
            system_address = real_estate_blockchain.real_estate_blockchain_system()[
                "address"]
            new_trx = {
                "sender": system_address,
                "receiver": miner_node.node_address,
                "value": 5000,
            }

            response = requests.post(
                f"{miner_node.node_url}/mine_new_block_by_winner_node/",
                data=json.dumps({"mined_by": miner_node.node_name,
                                 "new_trx": new_trx, }),
                headers={"Content-Type": "application/json",
                         "X-CSRFToken": csrf_token})
            # print(response)

    return {
        "status": True,
        "message": f"ملک شما با موفقیت به توکن تبدیل شد وتراکنش مربوطه در بلوک شماره {create_new_transaction.get('block_index')} قرار گرفت و به محض این که بلوک مورد نظر در شبکه بلاکچین قرار گیرد توکن شما در بازار املاک منتشر خواهد شد.",
    }


def signature_verification(data: dict):
    property_signature = data.get("signature")
    property_information: dict = data.get("property_information")
    message_str: str = json.dumps(property_information)

    current_property: propertyModel = propertyModel.objects.filter(
        id__exact=property_information.get("property_id")).first()

    sender_public_key_str: str = current_property.property_creator.wallet.public_key[
        2:-1]
    sender_public_key_str = str(
        sender_public_key_str).split("\\n")

    sender_public_key_PEM = """"""
    for item in sender_public_key_str:
        sender_public_key_PEM += item + "\n"

    sender_public_key = pem_to_public_key(
        public_key_pem=sender_public_key_PEM.encode())

    verify_result: bool = verify_signature(
        public_key=sender_public_key, signature=bytes.fromhex(property_signature), message=message_str)
    if verify_result:
        current_sender: userModel = userModel.objects.filter(
            wallet__wallet_address__iexact=property_information.get("sender")).first()
        if float(current_sender.wallet.inventory) >= float(data.get("transaction_fee")) and current_sender.wallet.wallet_address == current_property.property_owner_address:
            return True
        else:
            return False
    else:
        return False


def verify_tokenization_transaction(data: dict):

    result: bool = signature_verification(data=data)
    # print(result)
    if result:
        verification_counter = 0
        nodes: nodeModel = nodeModel.objects.filter(is_disable=False).all()
        for node in nodes:
            node: nodeModel
            csrf_token = csrf.get_token(request=HttpRequest())
            response = requests.post(
                f"{node.node_url}/verification_transaction_by_nodes/",
                data=json.dumps(data),
                headers={"Content-Type": "application/json",
                         "X-CSRFToken": csrf_token})
            if response.json()["status"]:
                verification_counter += 1
        if verification_counter >= (nodes.count())*2 / 3:
            return True
        else:
            return False

    else:
        return False


class tokenizationView(View):
    @csrf_exempt
    def post(self, request: HttpRequest):
        received_data: dict = json.loads(request.body)
        if verify_tokenization_transaction(data=received_data):
            response_data = create_token(data=received_data)
        else:
            response_data = {
                "status": False,
                "message": "خطا در تایید امضای مالک!!"
            }
        return JsonResponse(response_data)


@csrf_exempt
def create_signature_to_tokenization(request: HttpRequest):
    if request.method == "POST":
        try:
            data: dict = json.loads(request.body)
            property_id = data.get("property_id")
            current_property: propertyModel = propertyModel.objects.filter(
                id__exact=property_id).first()
            if current_property:
                sender: str = current_property.property_creator.wallet.wallet_address
                receiver: str = smart_contract_address(
                    contract_name="propertyـtokenization_function")
                property_information: dict = {
                    "sender": sender,
                    "receiver": receiver,
                    "property_id": property_id,
                }
                message_str: str = json.dumps(property_information)
                sender_private_key_str: str = current_property.property_creator.wallet.private_key[
                    2:-1]
                sender_private_key_str = str(
                    sender_private_key_str).split("\\n")
                sender_private_key_PEM = """"""
                for item in sender_private_key_str:
                    sender_private_key_PEM += item + "\n"

                sender_private_key = pem_to_private_key(
                    private_key_pem=sender_private_key_PEM.encode())
                signature = create_signature(private_key=sender_private_key,
                                             message=message_str)["signature_hex"]
                # print(signature)
                # print(bytes.fromhex(signature))
                # print(message_str)
                return JsonResponse({
                    "status": True,
                    "property_information": property_information,
                    "signature": signature,
                    "message": "signature successful."
                })
            else:
                return JsonResponse({
                    "status": False,
                    "message": "signature unsuccessful !!"
                })
        except Exception as error:
            print(error)
            return JsonResponse({
                "status": False,
                "error": error,
            })


# ///////////////////////////////////////////////////////////////

@csrf_exempt
def update_transactions(request: HttpRequest):
    if request.method == "POST":
        data: dict = json.loads(request.body)
        real_estate_blockchain.real_estate_transactions.append(
            data.get("transaction"))
        # print(real_estate_blockchain.real_estate_transactions)
        return JsonResponse({"status": True})


@csrf_exempt
def verification_transaction_by_nodes(request: HttpRequest):
    if request.method == "POST":
        data: dict = json.loads(request.body)
        # print(data)
        result: bool = signature_verification(data=data)
        # print(result)
        return JsonResponse({"status": True})


@csrf_exempt
def mine_new_block_by_winner_node(request: HttpRequest):
    if request.method == "POST":
        data: dict = json.loads(request.body)

        previous_block = real_estate_blockchain.get_last_block()
        previous_proof = previous_block["block_proof_number"]
        new_proof = real_estate_blockchain.proof_of_work(previous_proof)
        nodes: nodeModel = nodeModel.objects.filter(is_disable=False).all()
        verification_counter = 0

        for node in nodes:
            csrf_token = csrf.get_token(request=HttpRequest())
            node: nodeModel
            response = requests.post(
                url=f"{node.node_url}/verify_proof_of_work_by_nodes/",
                data=json.dumps({
                    "previous_proof": previous_proof,
                    "new_proof": new_proof["new_proof"],
                }),
                headers={"Content-Type": "application/json",
                         "X-CSRFToken": csrf_token})
            if response.json()["status"]:
                # print(response.json()["status"])
                verification_counter += 1
        if verification_counter >= (nodes.count())*2 / 3:
            previous_hash = real_estate_blockchain.hash(previous_block)
            new_block = real_estate_blockchain.create_block(proof=new_proof["new_proof"], previous_block_hash=previous_hash, miner_address=data.get(
                "mined_by"), block_nonce=new_proof["hash_operation"])
            new_transaction: transactionsModel = real_estate_blockchain.add_transaction(
                transaction_info={
                    "transaction_type": "miner_reward",
                    "new_trx": data.get("new_trx"),
                })
            real_estate_blockchain.real_estate_transactions.append(
                new_transaction.transaction_information()
            )

            for transaction in real_estate_blockchain.real_estate_transactions:
                print(transaction.get("transaction_id"))

        else:
            pass

    real_estate_blockchain.replace_chain()
    # print(real_estate_blockchain.real_estate_chain)

    return JsonResponse({
        "status": True,
    })
    # real_estate_blockchain.create_block(
    #     proof=2, previous_block_hash="0x5trdfu6rgser4ger4g6hsb54s")
    # for trx in real_estate_blockchain.real_estate_transactions:
    #     for field in trx.trx_status.all():
    #         field.published = True
    #         field.save()

    # print(real_estate_blockchain.real_estate_transactions.count())


# /////////////////////////////////////////////////////

class getChainView(View):
    def get(self, request: HttpRequest):
        response = {
            "chain": real_estate_blockchain.real_estate_chain,
            "length": len(real_estate_blockchain.real_estate_chain),
        }
        # print(real_estate_blockchain.real_estate_transactions)

        return JsonResponse(response)


@csrf_exempt
def updateChainView(request: HttpRequest):
    if request.method == "POST":
        data: dict = json.loads(request.body)
        real_estate_blockchain.real_estate_chain = data.get("chain")
        return JsonResponse({"true": True})


# //////////////////////////////////////////////////////////////////

@csrf_exempt
def verify_proof_of_work_by_nodes(request: HttpRequest):
    if request.method == "POST":
        data: dict = json.loads(request.body)
        result = real_estate_blockchain.proof_of_work(new_proof=data.get(
            "new_proof"), previous_proof=data.get("previous_proof"))
        status = False
        if result.get("new_proof") == data.get("new_proof"):
            status = True
    return JsonResponse({
        "status": status,
    })
