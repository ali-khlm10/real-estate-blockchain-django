from django.contrib import admin
from .models import buyRequestModel, buyRequestStatusModel, accept_rejectBuyRequestModel, buyModel, buyStatusModel
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


class buyAdmin(admin.ModelAdmin):
    list_display = [
        "finalizing_buy_by",
        "finalizing_buy_to",
    ]


class buyStatusAdmin(admin.ModelAdmin):
    list_display = [
        "pending",
        "is_finalized",
    ]


admin.site.register(buyRequestModel, buyRequestAdmin)
admin.site.register(buyRequestStatusModel, buyRequestStatusAdmin)
admin.site.register(accept_rejectBuyRequestModel, accept_rejectBuyRequestAdmin)
admin.site.register(buyModel, buyAdmin)
admin.site.register(buyStatusModel, buyStatusAdmin)
