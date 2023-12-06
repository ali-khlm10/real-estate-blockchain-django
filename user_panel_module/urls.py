from django.urls import path

from . import views

urlpatterns = [
    path("user_dashboard/", views.userDashboardView.as_view(), name='user-dashboard'),
    path("user_properties/", views.userPropertiesView.as_view(), name='user-properties'),
    path("received_requests/", views.receivedRequestsView.as_view(), name='received-requests'),
    path("sended_requestes/", views.sendedRequestsView.as_view(), name='sended-requestes'),
    path("user_wallet/", views.userWalletView.as_view(), name='user-wallet'),
    
]
