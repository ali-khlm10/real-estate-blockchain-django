from django.urls import path
from . import views
urlpatterns = [
    path("blocks/", views.blocksView.as_view(), name="blocks-page"),
    path("transactions/", views.transactionsView.as_view(), name="trxs-page"),

    path("block/<int:block_number>", views.blockView.as_view(), name="block"),
    path("hash/<str:trx_hash>", views.trxView.as_view(), name="trx"),

    path("serach/", views.searchInformationView.as_view(), name="search-page"),
    path("user_info/", views.searchUserInformationView.as_view(), name="user-info"),
    path("token_info/", views.searchTokenInformationView.as_view(), name="token-info"),
]
