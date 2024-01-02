from django.contrib import admin
from .models import buyRequestModel, buyRequestStatusModel
# Register your models here.


class buyRequestAdmin(admin.ModelAdmin):
    list_display = [
        "buy_request_from",
        "buy_request_to",
    ]


class buyRequestStatusAdmin(admin.ModelAdmin):
    list_display = [
        "pending",
        "is_accepted",
        "is_rejected",
    ]


admin.site.register(buyRequestModel, buyRequestAdmin)
admin.site.register(buyRequestStatusModel, buyRequestStatusAdmin)
