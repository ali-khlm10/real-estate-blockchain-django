from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from token_module.models import propertyTokenModel
from utils.generate_pair_key import pem_to_private_key, pem_to_public_key
from utils.create_and_verify_signature import create_signature, verify_signature

# Create your views here.


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

        return JsonResponse({
            "status": True,
            "message": "تراکنش مربوطه در بلاک شماره ... قرار گرفت",
        })


# //////////////////////////////////////////////////////////////////////////
