from django.urls import path
from . import views

urlpatterns = [
    path('create_signature_to_tokenization/', views.create_signature_to_tokenization,
         name="create-signature-to-tokenization"),
]
