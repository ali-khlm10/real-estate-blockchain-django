from django.contrib import admin
from . import models
# Register your models here.


class propertyTokenAdmin(admin.ModelAdmin):
    list_display = [
        "token_id",
    ]


admin.site.register(models.propertyTokenModel, propertyTokenAdmin)
