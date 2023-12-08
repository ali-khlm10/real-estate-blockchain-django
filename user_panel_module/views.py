from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404, HttpResponseNotFound
from django.urls import reverse


from django.views import View

from account_module.models import userModel

from property_module.models import propertyModel, propertyStatusModel

# Create your views here.


class userDashboardView(View):
    def get(self, request: HttpRequest):
        current_user: userModel = userModel.objects.filter(
            id=request.user.id).first()
        if current_user and not current_user.is_superuser:
            context = {
                "current_user": current_user,
            }
            return render(request, "user_panel_module/user_dashboard.html", context)
        else:
            if current_user.is_superuser:
                return redirect(reverse('admin:index'))
            raise HttpResponseNotFound()


class userPropertiesView(View):
    def get(self, request: HttpRequest):
        current_user: userModel = userModel.objects.filter(
            id=request.user.id).first()
        user_properties: propertyModel = propertyModel.objects.filter(
            property_creator__exact=current_user).all()
        context = {
            "user_properties": user_properties,
        }
        return render(request, "user_panel_module/user_properties.html", context)

# //////////////////////////////////////////////////////////////////


class agentReceivedRequestsView(View):
    def get(self, request: HttpRequest):
        current_user: userModel = userModel.objects.filter(
            id__exact=request.user.id).first()
        if current_user.is_gov_agent:
            agent_request_received: propertyModel = propertyModel.objects.all()
            context = {
                "agent_request_received": agent_request_received,
            }
            return render(request, "user_panel_module/agent_received_requests.html", context)
        else:
            raise Http404()


class agentAcceptRequestView(View):
    def get(self, request: HttpRequest, property_id: int):
        current_user: userModel = userModel.objects.filter(
            id__exact=request.user.id).first()

        current_property: propertyModel = propertyModel.objects.filter(
            id__exact=property_id).first()
        current_property_status: propertyStatusModel = propertyStatusModel.objects.filter(
            property__exact=current_property).first()

        if current_user.is_gov_agent:
            current_property_status.pending = False
            current_property_status.accepted = True
            current_property_status.pending = False

            current_property.is_verified = True
            current_property.property_owner_address = current_property.property_creator.wallet.wallet_address

            current_property_status.save()
            current_property.save()
            return redirect(reverse("agent-received-requests"))
        else:
            raise Http404()


class agentRejectRequestView(View):
    def get(self, request: HttpRequest, property_id: int):
        current_property: propertyModel = propertyModel.objects.filter(
            id__exact=property_id).first()
        current_property_status: propertyStatusModel = propertyStatusModel.objects.filter(
            property__exact=current_property).first()
        current_property_status.pending = False
        current_property_status.accepted = False
        current_property_status.rejected = True
        current_property.is_verified = False
        current_property_status.save()
        current_property.save()
        return redirect(reverse("agent-received-requests"))
# ///////////////////////////////////////////////////////////////////////


class receivedRequestsView(View):
    def get(self, request: HttpRequest):
        context = {}
        return render(request, "user_panel_module/received_requests.html", context)


class sendedRequestsView(View):
    def get(self, request: HttpRequest):
        context = {}
        return render(request, "user_panel_module/sended_requests.html", context)


class userWalletView(View):
    def get(self, request: HttpRequest):
        context = {}
        return render(request, "user_panel_module/user_wallet.html", context)


def user_panel_menu_component(request: HttpRequest):
    current_user: userModel = userModel.objects.filter(
        id=request.user.id).first()
    context = {
        "current_user": current_user,
    }
    return render(request, 'user_panel_module/components/user_panel_menu_component.html', context)
