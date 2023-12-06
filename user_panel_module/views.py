from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404, HttpResponseNotFound
from django.urls import reverse


from django.views import View

from account_module.models import userModel

from property_module.models import propertyModel, propertyDetailesModel

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
