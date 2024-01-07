from django.urls import path
from . import views


urlpatterns = [
    path("create_signature_to_buy_request/", views.create_signature_to_buy_request,
         name="create-signature-to-buy-request"),
    path("buying_request/", views.buying_request,
         name="buying-request"),
    path("verification_buy_request_transaction_by_nodes/", views.verification_buy_request_transaction_by_nodes,
         name="verification-buy-request-transaction-by-nodes"),


    path("create_signature_to_accept_reject_buy_request/", views.create_signature_to_accept_reject_buy_request,
         name="create-signature-to-accept-reject-buy-request"),
    path("accepting_buy_request/", views.accepting_buy_request,
         name="accepting-buy-request"),
    path("rejecting_buy_request/", views.rejecting_buy_request,
         name="rejecting-buy-request"),
    path("verification_accept_reject_buy_request_transaction_by_nodes/", views.verification_accept_reject_buy_request_transaction_by_nodes,
         name="verification-accept-reject-buy-request-transaction-by-nodes"),

]
