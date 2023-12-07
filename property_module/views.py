from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpRequest
from .forms import propertyForm
from account_module.models import userModel
from .models import propertyModel, propertyDetailesModel, propertyStatusModel
# Create your views here.


class createPropertyView(View):
    def get(self, request: HttpRequest):
        property_form: propertyForm = propertyForm()

        context = {
            "property_form": property_form,
        }
        return render(request, 'user_panel_module/create_property.html', context)

    def post(self, request: HttpRequest):
        property_form: propertyForm = propertyForm(request.POST, request.FILES)

        if property_form.is_valid():
            current_user: userModel = userModel.objects.filter(
                id=request.user.id).first()

            current_title = request.POST.get('title')
            current_type = request.POST.get('type')
            current_length = request.POST.get('length')
            current_price = request.POST.get('price')
            current_short_description = request.POST.get('short_description')
            current_image = request.FILES["image"]
            current_description = request.POST.get('description')
            current_address = request.POST.get('address')
            new_property_detailes: propertyDetailesModel = propertyDetailesModel.objects.create(
                property_title=current_title,
                property_type=current_type,
                property_length=current_length,
                property_price=current_price,
                property_short_description=current_short_description,
                property_image=current_image,
                property_description=current_description,
                property_address=current_address,
            )
            new_property_detailes.save()

            new_property: propertyModel = propertyModel.objects.create(
                property_detailes=new_property_detailes,
                property_creator=current_user,
            )
            new_property.save()

            new_property_status: propertyStatusModel = propertyStatusModel.objects.create(
                property=new_property,
            )
            new_property_status.save()

            return redirect(reverse("user-properties"))
        context = {
            "property_form": property_form,
        }
        return render(request, 'user_panel_module/create_property.html', context)
