from django.urls import path
from . import views

urlpatterns = [
    path('create_property_sign/', views.createPropertySignature,
         name="create-property-sign"),
]
