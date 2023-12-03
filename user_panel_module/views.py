from django.shortcuts import render
from django.http import HttpRequest

from django.views import View

# Create your views here.


class userDashboardView(View):
    def get(self, request : HttpRequest):
        context = {}
        return render(request,"user_panel_module/user_dashboard.html",context)


class createPropertyView(View):
    def get(self, request : HttpRequest):
        context = {}
        return render(request,"user_panel_module/create_property.html",context)
    
    

class userPropertiesView(View):
    def get(self, request : HttpRequest):
        context = {}
        return render(request,"user_panel_module/user_properties.html",context)
    


class receivedRequestsView(View):
    def get(self, request : HttpRequest):
        context = {}
        return render(request,"user_panel_module/received_requests.html",context)
    
    
    
class sendedRequestsView(View):
    def get(self, request : HttpRequest):
        context = {}
        return render(request,"user_panel_module/sended_requests.html",context)



def user_panel_menu_component(request: HttpRequest):
    return render(request, 'user_panel_module/components/user_panel_menu_component.html')