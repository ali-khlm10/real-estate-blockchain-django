from django.contrib import admin
from .models import buyRequestModel, buyRequestStatusModel, accept_rejectBuyRequestModel
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


class accept_rejectBuyRequestAdmin(admin.ModelAdmin):
    list_display = [
        "accept_reject_status",
        "accept_reject_buy_request_by",
        "accept_reject_buy_request_to",
    ]


admin.site.register(buyRequestModel, buyRequestAdmin)
admin.site.register(buyRequestStatusModel, buyRequestStatusAdmin)
admin.site.register(accept_rejectBuyRequestModel, accept_rejectBuyRequestAdmin)
