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

    path("get_chain/", views.getChainView.as_view(), name="get-chain"),

    path("update_chain/", views.updateChainView, name="update-chain"),
    path("update_transactions/", views.update_transactions,
         name="update-transactions"),

    path("verify_proof_of_work_by_nodes/", views.verify_proof_of_work_by_nodes,
         name="verify-proof-of-work-by-nodes"),
]
