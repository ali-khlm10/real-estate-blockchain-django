from django.urls import path
from . import views

urlpatterns = [
    path("create_property/", views.createPropertyView.as_view(),
         name="create-property"),
    path("property_detailes/<int:property_id>", views.propertyDetailesPageView.as_view(),
         name="property-detailes"),
]
