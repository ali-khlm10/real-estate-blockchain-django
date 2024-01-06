from django.db import models

from token_module.models import propertyTokenModel

# Create your models here.


class buyRequestModel(models.Model):
    buy_request_from = models.CharField(
        verbose_name="درخواست از", max_length=500, null=True, blank=True)
    buy_request_to = models.CharField(
        verbose_name="درخواست به", max_length=500, null=True, blank=True)
    token = models.ForeignKey(to=propertyTokenModel, verbose_name="شماره توکن",
                              on_delete=models.CASCADE, related_name="token", null=True, blank=True)
    buy_request_created_date = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="زمان ایجاد درخواست خرید ملک", null=True, blank=True)
    buy_request_prepayment = models.FloatField(
        verbose_name="مقدار بیعانه پیشنهادی", default=0)

    class Meta:
        verbose_name = "درخواست خرید"
        verbose_name_plural = "درخواست های خرید"

    def __str__(self):
        return self.token.token_id


class buyRequestStatusModel(models.Model):
    request = models.ForeignKey(to=buyRequestModel, verbose_name="درخواست",
                                on_delete=models.CASCADE, related_name="request", null=True, blank=True)
    pending = models.BooleanField(
        verbose_name="در انتظار پذیرش",  default=True)
    is_accepted = models.BooleanField(
        verbose_name="پذیرفته شده",  default=False)
    is_rejected = models.BooleanField(verbose_name="رد شده",  default=False)

    class Meta:
        verbose_name = "وضعیت درخواست خرید"
        verbose_name_plural = "وضعیت درخواست های خرید"

    def __str__(self):
        return self.request.token.token_id

    def status(self):
        if self.is_accepted:
            return "is_accepted"

        elif self.is_rejected:
            return "is_rejected"

        else:
            return "pending"


# //////////////////////////////////////////////////////////////
