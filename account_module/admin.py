from django.contrib import admin
from . import models
# Register your models here.



class userAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'email',
        'is_active',
    ]


class userWalletAdmin(admin.ModelAdmin):
    list_display = [
        'wallet_address',
        'inventory',
    ]


admin.site.register(models.userModel,userAdmin)
admin.site.register(models.userWalletModel,userWalletAdmin)