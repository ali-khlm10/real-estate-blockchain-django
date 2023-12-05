from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
# Create your models here.


class userWalletModel(models.Model):
    private_key = models.CharField(
        max_length=2000, verbose_name="کلید خصوصی", editable=False)
    public_key = models.CharField(
        max_length=2000, verbose_name="کلید عمومی", editable=False)
    wallet_address = models.CharField(
        max_length=2000, verbose_name="آدرس کیف پول", editable=False)
    inventory = models.FloatField(default=0.0, verbose_name="موجودی",)

    class Meta:
        verbose_name = "کیف پول"
        verbose_name_plural = "کیف پول کاربران"

    def __str__(self):
        return self.wallet_address


class userModel(AbstractUser):
    avatar = models.ImageField(upload_to="images/profile_avatar",
                               verbose_name="تصویر آواتار", blank=True, null=True)
    username = models.CharField(
        max_length=50, verbose_name="نام کاربری", unique=True)
    password = models.CharField(max_length=250, verbose_name="رمز")
    is_gov_agent = models.BooleanField(
        default=False, verbose_name="نماینده دولت")

    wallet = models.ForeignKey(to=userWalletModel, verbose_name="کیف پول",
                               on_delete=models.CASCADE, related_name="user_wallet", null=True, blank=True)

    class Meta:
        verbose_name = "کاریر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        if self.first_name is not "" and self.last_name is not "":
            return self.get_full_name()
        else:
            return self.username

    def userInfo(self):
        information = {
            "username": self.username,
            "email": self.email,
            "avatar": self.avatar,
            "is_gov_agent": self.is_gov_agent,
            "wallet_address": self.wallet.wallet_address,
            "wallet_public_key": self.wallet.public_key,
            "wallet_private_key": self.wallet.private_key,
            "wallet_inventory": self.wallet.inventory,
        }
        return information
# //////////////////////////////////////////////////////////