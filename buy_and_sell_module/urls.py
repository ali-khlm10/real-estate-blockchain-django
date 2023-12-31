from django.urls import path
from . import views


urlpatterns = [
    path("create_signature_to_buy_request/", views.create_signature_to_buy_request,
         name="create-signature-to-buy-request"),
    path("buying_request/", views.buying_request,
        name="buying-request"),
]
