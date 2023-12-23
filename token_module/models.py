from django.db import models

from property_module.models import propertyModel

from account_module.models import userModel
# Create your models here.


class propertyTokenModel(models.Model):
    property_of_token: propertyModel = models.ForeignKey(
        to=propertyModel, verbose_name="ملک مربوط به توکن", on_delete=models.CASCADE, related_name="property_of_token", null=True, blank=True)
    property_owner_address: str = models.CharField(
        verbose_name="آدرس مالک توکن", max_length=500, null=True, blank=True)
    token_id = models.CharField(
        verbose_name="شماره توکن ملک", max_length=500, unique=True)
    token_created_date = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="زمان ایجاد توکن", null=True)
    is_published = models.BooleanField(
        verbose_name="منتشر شده/نشده", default=False)
    token_information = models.TextField(
        verbose_name="اطلاعات مربوط به توکن", null=True, blank=True)

    class Meta:
        verbose_name = "توکن"
        verbose_name_plural = "توکن ها"

    def __str__(self):
        return self.token_id


# ///////////////////////////////////////////////////////////


class smartContractModel(models.Model):
    contract_name = models.CharField(
        verbose_name="نام قرارداد هوشمند", max_length=250)
    contract_address = models.CharField(
        max_length=2000, verbose_name="آدرس قرارداد هوشمند", editable=False)
    contract_inventory = models.FloatField(
        default=0.0, verbose_name="موجودی قرارداد هوشمند",)
    nonce = models.IntegerField(verbose_name="تعداد دفعات فراخوانی", default=0)

    def counter(self):
        self.nonce += 1

    class Meta:
        verbose_name = "قرارداد هوشمند"
        verbose_name_plural = "قراردادهای هوشمند"

    def __str__(self):
        return self.contract_address
