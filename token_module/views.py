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
from .models import propertyTokenModel
import hashlib
# Create your views here.


def create_token_id(token_information):
    token_information_str: str = json.dumps(token_information)
    hex_hash = hashlib.sha512(
        token_information_str.encode('utf-8')).hexdigest()
    int_hash = int(hex_hash, 16)  # convert hexadecimal to integer

    return int_hash


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
    )
    new_token.save()
    current_property.token_generated = True
    current_property.save()
    return {
        "status": True,
        "message": "ملک شما با موفقیت به توکن تبدیل شد وتراکنش مربوطه در بلوک شماره 10 قرار گرفت و به محض این که بلوک مورد نظر در شبکه بلاکچین قرار گیرد توکن شما در بازار املاک منتشر خواهد شد.",
    }


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
        return True
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
