from django.urls import path

from . import views

urlpatterns = [
    path("user_dashboard/", views.userDashboardView.as_view(), name='user-dashboard'),
    path("create_property/", views.createPropertyView.as_view(), name='create-property'),
    path("user_properties/", views.userPropertiesView.as_view(), name='user-properties'),
    path("received_requests/", views.receivedRequestsView.as_view(), name='received-requests'),
    path("sended_requestes/", views.sendedRequestsView.as_view(), name='sended-requestes'),
    
]
