import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils.create_and_verify_signature import create_signature, verify_signature
from utils.generate_pair_key import pem_to_private_key, pem_to_public_key
from utils.smart_contract import smart_contract_address
from property_module.models import propertyModel
from account_module.models import userModel
from django.views import View
from utils.create_and_verify_signature import verify_signature
# Create your views here.


def verify_tokenization_transaction(data: dict):
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
        pass


class tokenizationView(View):
    @csrf_exempt
    def post(self, request: HttpRequest):
        received_data: dict = json.loads(request.body)
        verify_tokenization_transaction(data=received_data)
        return JsonResponse({
            "status": True,
            "redirect_url": "user_properteis/"
        })


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
                print(message_str)
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
