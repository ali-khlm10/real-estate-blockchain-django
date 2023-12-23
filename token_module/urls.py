from django.urls import path
from . import views

urlpatterns = [
    path('create_signature_to_tokenization/', views.create_signature_to_tokenization,
         name="create-signature-to-tokenization"),
    path("tokenization/", views.tokenizationView.as_view(), name="tokenization"),

    path("verification_transaction_by_nodes/", views.verification_transaction_by_nodes,
         name="verification-transaction-by-nodes"),

    path("mine_new_block_by_winner_node/", views.mine_new_block_by_winner_node,
         name="mine-new-block-by-winner-node"),
]
