from django.db import models

# Create your models here.


class nodeModel(models.Model):
    node_name = models.CharField(
        verbose_name="نام گره", max_length=50, unique=True)
    node_port = models.CharField(
        verbose_name="شماره پورت", max_length=50, unique=True)
    node_url = models.URLField(
        verbose_name="آدرس گره", max_length=200, unique=True)
    node_inventory = models.FloatField(
        verbose_name="موجودی حساب گره", default=0.0, editable=False)
    node_join_to_network = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="زمان ملحق شدن گره به شبکه", null=True, blank=True)

    class Meta:
        verbose_name = "گره"
        verbose_name_plural = "گره ها"

    def __str__(self):
        return self.node_url
