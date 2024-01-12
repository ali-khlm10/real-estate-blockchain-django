from django.urls import path
from . import views
urlpatterns = [
    path("blocks/", views.blocksView.as_view(), name="blocks-page"),
    path("transactions/", views.transactionsView.as_view(), name="trxs-page"),
]
