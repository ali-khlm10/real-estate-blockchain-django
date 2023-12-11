from django.db import models

from property_module.models import propertyModel

from account_module.models import userModel
# Create your models here.


class propertyTokenModel(models.Model):
    property_of_token: propertyModel = models.ForeignKey(
        to=propertyModel, verbose_name="ملک مربوط به توکن", on_delete=models.CASCADE, related_name="property_of_token")
    property_owner_address: str = models.CharField(
        verbose_name="آدرس مالک توکن", max_length=500)
    token_id = models.CharField(
        verbose_name="شماره توکن ملک", max_length=500, unique=True)
    token_created_date = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="زمان ایجاد توکن", null=True)

    class Meta:
        verbose_name = "توکن"
        verbose_name_plural = "توکن ها"

    def __str__(self):
        return self.token_id
