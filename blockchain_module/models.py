from django.db import models

# Create your models here.


class blockModel(models.Model):
    block_number = models.IntegerField(verbose_name="شماره بلوک", default=0)
    block_timestamp = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="زمان ایجاد بلوک", null=True)
    mined_by = models.CharField(
        verbose_name="استخراج شده توسط", max_length=500, null=True, blank=True)
    block_reward = models.FloatField(verbose_name="پاداش بلوک", default=0.0)
    block_hash = models.CharField(
        verbose_name="هش بلوک", max_length=500, null=True, blank=True)
    previous_block_hash = models.CharField(
        verbose_name="هش بلوک قبلی", max_length=500, null=True, blank=True)
    block_nonce = models.IntegerField(
        verbose_name="شماره نانس بلوگ", default=0)
    block_proof_number = models.IntegerField(
        verbose_name="شماره اثبات کار بلوک", default=0)

    class Meta:
        verbose_name = "بلاک"
        verbose_name_plural = "بلاک ها"

    def __str__(self):
        return str(self.block_hash)


class blockStatusModel(models.Model):
    block = models.ForeignKey(to=blockModel, verbose_name="بلوک",
                              on_delete=models.CASCADE, related_name="block_status", null=True, blank=True)
    is_finalized = models.BooleanField(
        verbose_name="نهایی شده/نشده",  default=False)

    class Meta:
        verbose_name = "وضعیت بلاک"
        verbose_name_plural = "وضعیت بلاک ها"

    def __str__(self):
        return str(self.block.block_number)

    def status(self):
        return self.is_finalized


class transactionsModel(models.Model):
    transaction_from_address = models.CharField(
        verbose_name="از آدرس", max_length=500)
    transaction_to_address = models.CharField(
        verbose_name="به آدرس", max_length=500)
    transaction_hash = models.CharField(
        verbose_name="هش تراکنش", max_length=500)
    transaction_block = models.ForeignKey(
        to=blockModel, verbose_name="بلاک تراکنش", on_delete=models.CASCADE, null=True, blank=True, related_name="trx_block")
    transaction_timestamp = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="زمان ایجاد تراکنش", null=True)
    transaction_value = models.FloatField(
        verbose_name="مقدار انتقالی در تراکنش", default=0.0)
    transaction_fee = models.FloatField(
        verbose_name="هزینه تراکنش", default=0.0)
    transaction_type = models.CharField(
        verbose_name="نوع تراکنش", max_length=250)
    transaction_nonce = models.IntegerField(
        verbose_name="شماره نانس تراکنش", default=0)
    transaction_position_in_block = models.IntegerField(
        verbose_name="جایگاه تراکنش در بلاک", default=0)
    transaction_data = models.TextField(
        verbose_name="داده های اضافی تراکنش", null=True, blank=True)

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش ها"

    def __str__(self):
        return self.transaction_hash


class transactionStatusModel(models.Model):
    transaction = models.ForeignKey(to=transactionsModel, verbose_name="تراکنش",
                                    on_delete=models.CASCADE, related_name="trx_status", null=True, blank=True)
    pending = models.BooleanField(verbose_name="در صف انتشار",  default=True)
    published = models.BooleanField(verbose_name="منتشر شده",  default=False)
    not_published = models.BooleanField(
        verbose_name="منتشر نشده",  default=False)

    class Meta:
        verbose_name = "وضعیت تراکنش"
        verbose_name_plural = "وضعیت تراکنش ها"

    def __str__(self):
        return self.transaction.transaction_hash

    def status(self):
        if self.published:
            return "published"

        elif self.not_published:
            return "not_published"

        else:
            return "pending"


# ////////////////////////////////////////////////////


class blockchainModel(models.Model):
    blockchain_name = models.CharField(
        verbose_name="نام زنجیره بوکی", max_length=250)
    blockchain_address = models.CharField(
        verbose_name="آدرس سسیستم زنجیره بلوکی", max_length=500)
    blockchain_inventory = models.FloatField(
        verbose_name="موجودی سیستم زنجیره بلوکی", default=0.0)
