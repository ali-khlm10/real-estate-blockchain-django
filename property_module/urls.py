from django.urls import path
from . import views

urlpatterns = [
    path("create_property/", views.createPropertyView.as_view(),
         name="create-property"),
]
