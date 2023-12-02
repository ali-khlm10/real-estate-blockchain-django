from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.


class homeView(TemplateView):
    template_name = "home_module/home_page.html"
    
    



def site_header_partial(request):
    context = {}
    return render(request, "shared/site_header_partial.html", context=context)


def site_footer_partial(request):
    context = {}
    return render(request, "shared/site_footer_partial.html", context=context)