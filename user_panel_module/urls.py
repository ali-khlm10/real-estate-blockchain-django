from django.urls import path

from . import views

urlpatterns = [
    path("user_dashboard/", views.userDashboardView.as_view(), name='user-dashboard'),
    path("user_properties/", views.userPropertiesView.as_view(),
         name='user-properties'),

    path("agent_received_requests/", views.agentReceivedRequestsView.as_view(),
         name='agent-received-requests'),
    path("agent_accept_request/<int:property_id>",
         views.agentAcceptRequestView.as_view(), name='agent-accept-request'),
    path("agent_reject_request/<int:property_id>",
         views.agentRejectRequestView.as_view(), name='agent-reject-request'),

    path("received_requests/", views.receivedRequestsView.as_view(),
         name='received-requests'),
    path("sended_requestes/", views.sendedRequestsView.as_view(),
         name='sended-requestes'),
    path("user_wallet/", views.userWalletView.as_view(), name='user-wallet'),

    path('buy_result/<int:buy_id>',
         views.buyAndSellResultView.as_view(), name="buy-result"),
    path('sell_result/<int:buy_id>',
         views.buyAndSellResultView.as_view(), name="sell-result"),

]
