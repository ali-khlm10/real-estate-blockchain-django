from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View
from django.http import HttpRequest
from property_module.models import propertyModel


# Create your views here.


class homeView(View):
    def get(self, request: HttpRequest):
        properties: propertyModel = propertyModel.objects.filter(
            token_generated=True).order_by("-property_of_token__token_created_date")[:4]
        context = {
            "properties": properties
        }
        return render(request, "home_module/home_page.html", context)


def site_header_partial(request):
    context = {}
    return render(request, "shared/site_header_partial.html", context=context)


def site_footer_partial(request):
    context = {}
    return render(request, "shared/site_footer_partial.html", context=context)
