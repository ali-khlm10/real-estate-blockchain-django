from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from token_module.models import propertyTokenModel
from utils.generate_pair_key import pem_to_private_key, pem_to_public_key
from utils.create_and_verify_signature import create_signature, verify_signature
from account_module.models import userModel
from node_module.models import nodeModel
from utils.blockchain import real_estate_blockchain

from django.middleware import csrf
import requests

from .models import buyRequestModel, buyRequestStatusModel, accept_rejectBuyRequestModel
# Create your views
# here.


@csrf_exempt
def create_signature_to_buy_request(request: HttpRequest):
    if request.method == "POST":
        try:
            data: dict = json.loads(request.body)
            token_id: str = data.get("token_id")
            current_token: propertyTokenModel = propertyTokenModel.objects.filter(
                token_id__iexact=token_id).first()
            if current_token:
                sender: str = request.user.wallet.wallet_address
                receiver: str = current_token.property_owner_address
                buy_request_information = {
                    "sender": sender,
                    "receiver":  receiver,
                    "token_id": token_id,
                    "transaction_type": "buy_request",
                }
                message_str: str = json.dumps(buy_request_information)
                sender_private_key_str: str = request.user.wallet.private_key[2:-1]

                sender_private_key_str = str(
                    sender_private_key_str).split("\\n")

                sender_private_key_PEM = """"""
                for item in sender_private_key_str:
                    sender_private_key_PEM += item + "\n"

                sender_private_key = pem_to_private_key(
                    private_key_pem=sender_private_key_PEM.encode())

                signature = create_signature(private_key=sender_private_key,
                                             message=message_str)["signature_hex"]

                return JsonResponse({
                    "status": True,
                    "buy_request_information": buy_request_information,
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


def buying_request(request: HttpRequest):
    if request.method == "POST":
        data: dict = json.loads(request.body)
        if verify_buying_request_transaction(data=data):
            response_data = add_buy_request_trx_and_mine_block(data=data)

        else:
            response_data = {
                "status": False,
                "message": "خطا در تایید امضای مالک!!"
            }
        return JsonResponse(response_data)


def verify_buying_request_transaction(data: dict):

    result: bool = buy_request_signature_verification(data=data)
    # print(result)
    if result:
        verification_counter = 0
        nodes: nodeModel = nodeModel.objects.filter(is_disable=False).all()
        for node in nodes:
            node: nodeModel
            csrf_token = csrf.get_token(request=HttpRequest())
            response = requests.post(
                f"{node.node_url}/verification_buy_request_transaction_by_nodes/",
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


def buy_request_signature_verification(data: dict):
    buy_request_signature = data.get("signature")
    buy_request_prepayment = data.get("prepayment")
    buy_request_information: dict = data.get("buy_request_information")
    message_str: str = json.dumps(buy_request_information)

    current_sender: userModel = userModel.objects.filter(
        wallet__wallet_address__iexact=buy_request_information.get("sender")).first()

    sender_public_key_str: str = current_sender.wallet.public_key[2:-1]
    sender_public_key_str = str(
        sender_public_key_str).split("\\n")

    sender_public_key_PEM = """"""
    for item in sender_public_key_str:
        sender_public_key_PEM += item + "\n"

    sender_public_key = pem_to_public_key(
        public_key_pem=sender_public_key_PEM.encode())

    verify_result: bool = verify_signature(
        public_key=sender_public_key, signature=bytes.fromhex(buy_request_signature), message=message_str)

    if verify_result:
        if float(current_sender.wallet.inventory) >= float(data.get("transaction_fee")) + float(buy_request_prepayment):
            return True
        else:
            return False
    else:
        return False


def add_buy_request_trx_and_mine_block(data: dict):
    buy_request_information: dict = data.get("buy_request_information")
    sender = buy_request_information.get("sender")
    receiver = buy_request_information.get("receiver")
    token_id = buy_request_information.get("token_id")
    token: propertyTokenModel = propertyTokenModel.objects.filter(
        token_id__iexact=token_id).first()
    buy_request: buyRequestModel = buyRequestModel.objects.create()
    buy_request.buy_request_from = sender
    buy_request.buy_request_to = receiver
    buy_request.token = token
    buy_request.buy_request_prepayment = float(data.get("prepayment"))
    buy_request.save()
    buy_request_status: buyRequestStatusModel = buyRequestStatusModel.objects.create()
    buy_request_status.request = buy_request
    buy_request_status.save()

    create_new_transaction: dict = real_estate_blockchain.add_transaction(
        transaction_info={
            "transaction_type": "buy_request",
            "data": data,
            "transaction_fee": data.get("transaction_fee"),
            "transaction_prepayment": data.get("prepayment"),
        }
    )
    replace_transactions_result: bool = real_estate_blockchain.replace_transactions(
        trx=create_new_transaction.get("transaction"))

    if replace_transactions_result:
        # print(len(real_estate_blockchain.real_estate_transactions))
        if len(real_estate_blockchain.real_estate_transactions) == 1:
            miner_node: nodeModel = real_estate_blockchain.proof_of_stake()
            csrf_token = csrf.get_token(request=HttpRequest())
            system_address = real_estate_blockchain.real_estate_blockchain_system()[
                "address"]
            new_trx = {
                "sender": system_address,
                "receiver": miner_node.node_address,
                "value": 0.0,
            }

            response = requests.post(
                f"{miner_node.node_url}/mine_new_block_by_winner_node/",
                data=json.dumps({"mined_by": miner_node.node_address,
                                 "new_trx": new_trx, }),
                headers={"Content-Type": "application/json",
                         "X-CSRFToken": csrf_token})
            print(response)
            if response.json()["status"]:
                print("hello")
                real_estate_blockchain.real_estate_transactions = []
                real_estate_blockchain.real_estate_chain = real_estate_blockchain.get_real_estate_chain()

        return {
            "status": True,
            "message": f"درخواست خرید ملک شما با موفقیت انجام شد وتراکنش مربوطه در بلوک شماره {create_new_transaction.get('block_index')} قرار گرفت و به محض این که بلوک مورد نظر در شبکه بلاکچین قرار گیرد درخواست خرید ملک شما در اختیار مالک قرار خواهد گرفت.",
        }
    else:
        return {
            "status": False,
            "messge": "مشکلی در ایجاد بلوک به وجود آمده است."
        }


@csrf_exempt
def verification_buy_request_transaction_by_nodes(request: HttpRequest):
    if request.method == "POST":
        data: dict = json.loads(request.body)
        # print(data)
        result: bool = buy_request_signature_verification(data=data)
        print(result)
        if result:
            return JsonResponse({"status": True})
        else:
            return JsonResponse({"status": False})


# //////////////////////////////////////////////////////////////////////////

@csrf_exempt
def create_signature_to_accept_reject_buy_request(request: HttpRequest):
    if request.method == "POST":
        try:
            data: dict = json.loads(request.body)
            token_id: str = data.get("token_id")
            buyer_address: str = data.get("buyer_address")
            operation: str = data.get("operation")
            current_token: propertyTokenModel = propertyTokenModel.objects.filter(
                token_id__iexact=token_id).first()
            if current_token:
                if operation == "accepting":
                    sender: str = request.user.wallet.wallet_address
                    receiver: str = buyer_address
                    accept_reject_buy_request_information = {
                        "sender": sender,
                        "receiver":  receiver,
                        "token_id": token_id,
                        "transaction_type": "accept_buy_request",
                    }
                else:
                    sender: str = request.user.wallet.wallet_address
                    receiver: str = buyer_address
                    accept_reject_buy_request_information = {
                        "sender": sender,
                        "receiver":  receiver,
                        "token_id": token_id,
                        "transaction_type": "reject_buy_request",
                    }

                message_str: str = json.dumps(
                    accept_reject_buy_request_information)
                sender_private_key_str: str = request.user.wallet.private_key[2:-1]

                sender_private_key_str = str(
                    sender_private_key_str).split("\\n")

                sender_private_key_PEM = """"""
                for item in sender_private_key_str:
                    sender_private_key_PEM += item + "\n"

                sender_private_key = pem_to_private_key(
                    private_key_pem=sender_private_key_PEM.encode())

                signature = create_signature(private_key=sender_private_key,
                                             message=message_str)["signature_hex"]

                return JsonResponse({
                    "status": True,
                    "accept_reject_buy_request_information": accept_reject_buy_request_information,
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


def accepting_buy_request(request: HttpRequest):
    if request.method == "POST":
        data: dict = json.loads(request.body)
        # print(data)
        if verify_accept_rejecting_buy_request_transaction(data=data):
            response_data = add_accept_buy_request_trx_and_mine_block(
                data=data)

        else:
            response_data = {
                "status": False,
                "message": "خطا در تایید امضای مالک!!"
            }
        return JsonResponse(response_data)


def rejecting_buy_request(request: HttpRequest):
    if request.method == "POST":
        data: dict = json.loads(request.body)
        # print(data)
        if verify_accept_rejecting_buy_request_transaction(data=data):
            response_data = add_reject_buy_request_trx_and_mine_block(
                data=data)

        else:
            response_data = {
                "status": False,
                "message": "خطا در تایید امضای مالک!!"
            }
        return JsonResponse(response_data)


def verify_accept_rejecting_buy_request_transaction(data: dict):

    result: bool = accept_reject_buy_request_signature_verification(data=data)
    # print(result)
    if result:
        verification_counter = 0
        nodes: nodeModel = nodeModel.objects.filter(is_disable=False).all()
        for node in nodes:
            node: nodeModel
            csrf_token = csrf.get_token(request=HttpRequest())
            response = requests.post(
                f"{node.node_url}/verification_accept_reject_buy_request_transaction_by_nodes/",
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


def accept_reject_buy_request_signature_verification(data: dict):
    accept_reject_buy_request_signature = data.get("signature")
    accept_reject_buy_request_information: dict = data.get(
        "accept_reject_buy_request_information")
    message_str: str = json.dumps(accept_reject_buy_request_information)

    current_sender: userModel = userModel.objects.filter(
        wallet__wallet_address__iexact=accept_reject_buy_request_information.get("sender")).first()

    sender_public_key_str: str = current_sender.wallet.public_key[2:-1]
    sender_public_key_str = str(
        sender_public_key_str).split("\\n")

    sender_public_key_PEM = """"""
    for item in sender_public_key_str:
        sender_public_key_PEM += item + "\n"

    sender_public_key = pem_to_public_key(
        public_key_pem=sender_public_key_PEM.encode())

    verify_result: bool = verify_signature(
        public_key=sender_public_key, signature=bytes.fromhex(accept_reject_buy_request_signature), message=message_str)

    if verify_result:
        if float(current_sender.wallet.inventory) >= float(data.get("transaction_fee")):
            return True
        else:
            return False
    else:
        return False


@csrf_exempt
def verification_accept_reject_buy_request_transaction_by_nodes(request: HttpRequest):
    if request.method == "POST":
        data: dict = json.loads(request.body)
        # print(data)
        result: bool = accept_reject_buy_request_signature_verification(
            data=data)
        print(result)
        if result:
            return JsonResponse({"status": True})
        else:
            return JsonResponse({"status": False})


def add_accept_buy_request_trx_and_mine_block(data: dict):
    accept_buy_request_information: dict = data.get(
        "accept_reject_buy_request_information")
    sender = accept_buy_request_information.get("sender")
    buyer = accept_buy_request_information.get("receiver")
    token_id = accept_buy_request_information.get("token_id")
    token: propertyTokenModel = propertyTokenModel.objects.filter(
        token_id__iexact=token_id).first()
    buy_request: buyRequestModel = buyRequestModel.objects.filter(
        token=token, buy_request_from=buyer, buy_request_to=sender).first()

    for item in buy_request.request.all():
        item: buyRequestStatusModel
        item.pending = False
        item.is_accepted = True
        item.is_rejected = False
        item.save()

    accept_buy_request: accept_rejectBuyRequestModel = accept_rejectBuyRequestModel.objects.create()
    accept_buy_request.buy_request = buy_request
    accept_buy_request.accept_reject_status = True
    accept_buy_request.accept_reject_buy_request_by = sender
    accept_buy_request.accept_reject_buy_request_to = buyer
    accept_buy_request.accepted_rejected_token = token
    accept_buy_request.save()

    create_new_transaction: dict = real_estate_blockchain.add_transaction(
        transaction_info={
            "transaction_type": "accept_buy_request",
            "data": data,
            "transaction_fee": data.get("transaction_fee"),
        }
    )

    replace_transactions_result: bool = real_estate_blockchain.replace_transactions(
        trx=create_new_transaction.get("transaction"))

    if replace_transactions_result:
        # print(len(real_estate_blockchain.real_estate_transactions))
        if len(real_estate_blockchain.real_estate_transactions) != 0:
            miner_node: nodeModel = real_estate_blockchain.proof_of_stake()
            csrf_token = csrf.get_token(request=HttpRequest())
            system_address = real_estate_blockchain.real_estate_blockchain_system()[
                "address"]
            new_trx = {
                "sender": system_address,
                "receiver": miner_node.node_address,
                "value": 0.0,
            }
            print()
            response = requests.post(
                f"{miner_node.node_url}/mine_new_block_by_winner_node/",
                data=json.dumps({"mined_by": miner_node.node_address,
                                 "new_trx": new_trx, }),
                headers={"Content-Type": "application/json",
                         "X-CSRFToken": csrf_token})
            print(response)
            if response.json()["status"]:
                print("hello")
                real_estate_blockchain.real_estate_transactions = []
                real_estate_blockchain.real_estate_chain = real_estate_blockchain.get_real_estate_chain()

        return {
            "status": True,
            "message": f"درخواست خریدار مورد نظر پذیرفته شد و تراکنش مربوطه در بلوک شماره {create_new_transaction.get('block_index')} قرار گرفت و به محض این که بلوک مورد نظر در شبکه بلاکچین قرار گیرد نتیجه به خریدار اعلام خواهد شد.",
        }
    else:
        return {
            "status": False,
            "messge": "مشکلی در ایجاد بلوک به وجود آمده است."
        }


def add_reject_buy_request_trx_and_mine_block(data: dict):
    reject_buy_request_information: dict = data.get(
        "accept_reject_buy_request_information")

    sender = reject_buy_request_information.get("sender")
    buyer = reject_buy_request_information.get("receiver")
    token_id = reject_buy_request_information.get("token_id")
    token: propertyTokenModel = propertyTokenModel.objects.filter(
        token_id__iexact=token_id).first()
    buy_request: buyRequestModel = buyRequestModel.objects.filter(
        token=token, buy_request_from=buyer, buy_request_to=sender).first()


    for item in buy_request.request.all():
        item: buyRequestStatusModel
        item.pending = False
        item.is_accepted = False
        item.is_rejected = True
        item.save()

    reject_buy_request: accept_rejectBuyRequestModel = accept_rejectBuyRequestModel.objects.create()
    reject_buy_request.buy_request = buy_request
    reject_buy_request.accept_reject_buy_request_by = sender
    reject_buy_request.accept_reject_buy_request_to = buyer
    reject_buy_request.accepted_rejected_token = token
    reject_buy_request.save()

    create_new_transaction: dict = real_estate_blockchain.add_transaction(
        transaction_info={
            "transaction_type": "reject_buy_request",
            "data": data,
            "transaction_fee": data.get("transaction_fee"),
        }
    )

    replace_transactions_result: bool = real_estate_blockchain.replace_transactions(
        trx=create_new_transaction.get("transaction"))

    if replace_transactions_result:
        # print(len(real_estate_blockchain.real_estate_transactions))
        if len(real_estate_blockchain.real_estate_transactions) != 0:      
            miner_node: nodeModel = real_estate_blockchain.proof_of_stake()
            csrf_token = csrf.get_token(request=HttpRequest())
            system_address = real_estate_blockchain.real_estate_blockchain_system()[
                "address"]
            new_trx = {
                "sender": system_address,
                "receiver": miner_node.node_address,
                "value": 0.0,
            }

            response = requests.post(
                f"{miner_node.node_url}/mine_new_block_by_winner_node/",
                data=json.dumps({"mined_by": miner_node.node_address,
                                 "new_trx": new_trx, }),
                headers={"Content-Type": "application/json",
                         "X-CSRFToken": csrf_token})
            print(response)
            if response.json()["status"]:
                print("hello")
                real_estate_blockchain.real_estate_transactions = []
                real_estate_blockchain.real_estate_chain = real_estate_blockchain.get_real_estate_chain()

        return {
            "status": True,
            "message": f"درخواست خریدار مورد نظر توسط شما رد شد و تراکنش مربوطه در بلوک شماره {create_new_transaction.get('block_index')} قرار گرفت و به محض این که بلوک مورد نظر در شبکه بلاکچین قرار گیرد نتیجه به خریدار اعلام خواهد شد.",
        }
    else:
        return {
            "status": False,
            "messge": "مشکلی در ایجاد بلوک به وجود آمده است."
        }
