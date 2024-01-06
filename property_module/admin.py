from django.contrib import admin
from .models import propertyModel, propertyDetailesModel, propertyStatusModel
# Register your models here.


class propertyAdmin(admin.ModelAdmin):
    list_display = [
        'property_detailes',
        'property_creator',
        'is_verified',
        'token_generated',
    ]

    list_editable = [
        'is_verified',
        'token_generated',
    ]


class propertyDetailesAdmin(admin.ModelAdmin):
    list_display = [
        'property_title',
        'property_price',
    ]


class propertyStatusAdmin(admin.ModelAdmin):
    list_display = [
        'property',
        'pending',
        'accepted',
        'rejected',
    ]


admin.site.register(propertyModel, propertyAdmin)
admin.site.register(propertyDetailesModel, propertyDetailesAdmin)
admin.site.register(propertyStatusModel, propertyStatusAdmin)
