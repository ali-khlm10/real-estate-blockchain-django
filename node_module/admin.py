from django.contrib import admin
from . import models
from django.http import HttpRequest
from typing import Any
from utils.nodes import create_node_address, create_and_update_nodes

# Register your models here.


class nodeAdmin(admin.ModelAdmin):
    list_display = [
        'node_name',
        'node_port',
        'node_url',
        'node_inventory',
        'is_disable',
    ]

    list_editable = [
        'is_disable',
    ]

    def save_model(self, request: HttpRequest, obj: models.nodeModel, form: Any, change: Any) -> None:
        print('request:', request)
        print('object:', obj)
        print('change:', change)
        print('user:', request.user)
        if not change:
            obj.node_address = create_node_address(
                info={
                    "node_name": obj.node_name,
                    "node_port": obj.node_port,
                    "node_url": obj.node_url,
                    "node_inventory": obj.node_inventory,
                })

        if change:
            create_and_update_nodes()

        return super().save_model(request, obj, form, change)


admin.site.register(models.nodeModel, nodeAdmin)
