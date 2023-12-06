from django.contrib import admin
from .models import propertyModel,propertyDetailesModel
# Register your models here.


class propertyAdmin(admin.ModelAdmin):
    list_display = [
        'property_creator',
        'is_verified',
        'token_generated',
    ]
    
    

class propertyDetailesAdmin(admin.ModelAdmin):
    list_display = [
        'property_title',
        'property_price',
    ]
    

admin.site.register(propertyModel,propertyAdmin)
admin.site.register(propertyDetailesModel,propertyDetailesAdmin)