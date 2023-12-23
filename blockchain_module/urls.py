from django.urls import path
from . import views
urlpatterns = [
    path("blockchain/", views.blockchainView.as_view(), name="blockchain"),
]
