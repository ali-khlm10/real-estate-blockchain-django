from django.contrib import admin
from . import models
# Register your models here.


class nodeAdmin(admin.ModelAdmin):
    list_display = [
        'node_name',
        'node_port',
        'node_url',
        'node_inventory',
    ]


admin.site.register(models.nodeModel, nodeAdmin)
