from django.db import models
from account_module.models import userModel
# Create your models here.


class propertyDetailesModel(models.Model):
    property_title = models.CharField(verbose_name="عنوان ملک", max_length=50)
    property_type = models.CharField(verbose_name="نوع ملک", max_length=50)
    property_length = models.FloatField(verbose_name="متراژ ملک", default=0.0)
    property_price = models.FloatField(verbose_name="قیمت ملک", default=0.0)
    property_short_description = models.CharField(
        verbose_name="توضیحات کوتاه", max_length=200)
    property_image = models.ImageField(
        verbose_name="تصویر ملک", upload_to="property_images/", blank=True, null=True)
    property_description = models.TextField(verbose_name="توضیحات کامل")
    property_address = models.TextField(verbose_name="آدرس ملک")

    class Meta:
        verbose_name = "جزئیات ملک"
        verbose_name_plural = "جزئیات ملک ها"

    def __str__(self):
        return self.property_title

    def detailes(self):
        property = {
            "property_title": self.property_title,
            "property_type": self.property_type,
            "property_length": self.property_length,
            "property_price": self.property_price,
            "property_short_description": self.property_short_description,
            "property_image": self.property_image,
            "property_description": self.property_description,
            "property_address": self.property_address,
        }
        return property


class propertyModel(models.Model):
    property_detailes = models.ForeignKey(to=propertyDetailesModel, verbose_name="جزئیات ملک",
                                          on_delete=models.CASCADE, related_name="property_detailes")
    property_creator = models.ForeignKey(to=userModel, verbose_name="ایجاد کننده ملک",
                                         on_delete=models.CASCADE, related_name="property_creator")
    property_owner_address = models.CharField(
        verbose_name="آدرس مالک ملک", max_length=500, null=True, blank=True)
    is_verified = models.BooleanField(
        verbose_name="ملک تایید شده/تایید نشده", default=False)
    token_generated = models.BooleanField(
        verbose_name="توکن صادر شده/صادر نشده",  default=False)
    property_created_date = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="زمان ایجاد ملک", null=True, blank=True)

    class Meta:
        verbose_name = "ملک"
        verbose_name_plural = "ملک ها"

    def __str__(self):
        return self.property_detailes.property_title
