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

class accept_rejectBuyRequestModel(models.Model):
    buy_request = models.ForeignKey(to=buyRequestModel, verbose_name="درخواست خرید",
                                    on_delete=models.CASCADE, related_name="buy_request", null=True, blank=True)
    accept_reject_status = models.BooleanField(
        verbose_name="پذیرفته شده/نشده", default=False)
    accept_reject_buy_request_by = models.CharField(
        verbose_name="پذیرش یا رد درخواست خرید توسط", max_length=500, null=True, blank=True)
    accept_reject_buy_request_to = models.CharField(
        verbose_name="پذیرش یا رد درخواست خرید به", max_length=500, null=True, blank=True)
    accepted_rejected_token = models.ForeignKey(to=propertyTokenModel, verbose_name="شماره توکن پذیرفته شده/نشده",
                                                on_delete=models.CASCADE, related_name="accepted_rejected_token", null=True, blank=True)
    accepted_rejected_buy_request_date = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="زمان ایجاد پذیرش یا رد درخواست خرید ملک", null=True, blank=True)

    class Meta:
        verbose_name = "پذیرش یا رد درخواست خرید"
        verbose_name_plural = "پذیرش یا رد درخواست های خرید"

    def __str__(self):
        return self.accepted_rejected_token.token_id


# class accept_rejectbuyRequestStatusModel(models.Model):
#     accepted_rejected_request = models.ForeignKey(to=accept_rejectBuyRequestModel, verbose_name="درخواست پذیرفته شده/نشده",
#                                                   on_delete=models.CASCADE, related_name="accepted_rejected_request", null=True, blank=True)
#     pending = models.BooleanField(
#         verbose_name="در انتظار پاسخ",  default=True)
#     is_replyed = models.BooleanField(
#         verbose_name="پاسخ داده شده/نشده",  default=False)

#     class Meta:
#         verbose_name = "وضعیت درخواست خرید پذیرفته شده/نشده"
#         verbose_name_plural = "وضعیت درخواست های خرید پذیرفته شده/نشده"

#     def __str__(self):
#         return self.accepted_rejected_request.accepted_rejected_token.token_id

#     def status(self):
#         if self.is_replyed:
#             return "is_replyed"

#         else:
#             return "pending"


# //////////////////////////////////////////////


class buyModel(models.Model):
    accept_reject_buy_request = models.ForeignKey(to=accept_rejectBuyRequestModel, verbose_name="درخواست خرید پذیرفته شده/نشده",
                                                  on_delete=models.CASCADE, related_name="accept_reject_buy_request", null=True, blank=True)
    finalizing_buy_by = models.CharField(
        verbose_name="نهایی کردن خرید توسط", max_length=500, null=True, blank=True)
    finalizing_buy_to = models.CharField(
        verbose_name="نهایی کردن خرید به", max_length=500, null=True, blank=True)
    buyed_token = models.ForeignKey(to=propertyTokenModel, verbose_name="شماره توکن خریداری شده",
                                    on_delete=models.CASCADE, related_name="buyed_token", null=True, blank=True)
    finalizing_buy_date = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="زمان نهایی کردن خرید ملک", null=True, blank=True)

    class Meta:
        verbose_name = "خرید"
        verbose_name_plural = "خریدها"

    def __str__(self):
        return self.buyed_token.token_id


class buyStatusModel(models.Model):
    finalized_buy = models.ForeignKey(to=buyModel, verbose_name="خرید نهایی شده",
                                      on_delete=models.CASCADE, related_name="finalized_buy", null=True, blank=True)
    pending = models.BooleanField(
        verbose_name="در انتظار فروش",  default=True)
    is_finalized = models.BooleanField(
        verbose_name="نهایی شده",  default=False)

    class Meta:
        verbose_name = "وضعیت خرید"
        verbose_name_plural = "وضعیت خریدها"

    def __str__(self):
        return self.finalized_buy.buyed_token.token_id

    def status(self):
        if self.is_finalized:
            return "is finalized"

        else:
            return "pending"


# ////////////////////////////////////////////////////


class sellModel(models.Model):
    buy = models.ForeignKey(to=buyModel, verbose_name="خرید",
                            on_delete=models.CASCADE, related_name="buy", null=True, blank=True)
    finalizing_sell_by = models.CharField(
        verbose_name="نهایی کردن فروش توسط", max_length=500, null=True, blank=True)
    finalizing_sell_to = models.CharField(
        verbose_name="نهایی کردن فروش به", max_length=500, null=True, blank=True)
    selled_token = models.ForeignKey(to=propertyTokenModel, verbose_name="شماره توکن فروخته شده",
                                     on_delete=models.CASCADE, related_name="selled_token", null=True, blank=True)
    finalizing_sell_date = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="زمان نهایی کردن فروش ملک", null=True, blank=True)

    sell_status = models.BooleanField(
        verbose_name="وضعیت فروش", default=False)

    class Meta:
        verbose_name = "فروش"
        verbose_name_plural = "فروش ها"

    def __str__(self):
        return self.selled_token.token_id
