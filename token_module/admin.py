from django.contrib import admin
from . import models
# Register your models here.


class propertyTokenAdmin(admin.ModelAdmin):
    list_display = [
        "token_id",
    ]


class smartContractAdmin(admin.ModelAdmin):
    list_display = [
        "contract_name",
    ]


admin.site.register(models.propertyTokenModel, propertyTokenAdmin)
admin.site.register(models.smartContractModel, smartContractAdmin)
