from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpRequest
from .forms import *
from utils.generate_pair_key import generate_pair_key, pem_to_public_key
from utils.create_wallet_address import generate_wallet_address
from .models import userModel, userWalletModel
from django.contrib.auth import login, logout
# Create your views here.


class registerView(View):
    def get(self, request: HttpRequest):
        registeration_form: registerForm = registerForm()
        context = {
            "registeration_form": registeration_form,
        }
        return render(request, "account_module/register_page.html", context)

    def post(self, request: HttpRequest):
        registeration_form: registerForm = registerForm(
            request.POST, request.FILES)
        context = {
            "registeration_form": registeration_form,
        }
        if registeration_form.is_valid():
            # print(request.FILES["avatar"])
            pair_key = generate_pair_key()
            privat_key_pem, public_key_pem = pair_key["private_pem"], pair_key["public_pem"]
            wallet_address = generate_wallet_address(
                public_key=pem_to_public_key(public_key_pem=public_key_pem))
            new_user: userModel = userModel.objects.create(
                avatar=request.FILES["avatar"],
                username=request.POST.get("username"),
                email=request.POST.get("email"),
            )
            new_user.set_password(request.POST.get("password"))
            new_user_wallet: userWalletModel = userWalletModel.objects.create(
                private_key=privat_key_pem,
                public_key=public_key_pem,
                inventory=0.0,
                wallet_address=wallet_address,
            )
            new_user.wallet = new_user_wallet
            new_user.save()
            return redirect(reverse("login-page"))
        else:
            return render(request, "account_module/register_page.html", context)


class loginView(View):
    def get(self, request: HttpRequest):
        logination_form: loginForm = loginForm()
        context = {
            "logination_form": logination_form,
        }
        return render(request, "account_module/login_page.html", context)
    
    def post(self, request : HttpRequest):
        logination_form: loginForm = loginForm(request.POST)
        if logination_form.is_valid():
            current_user_email = logination_form.cleaned_data.get('email')
            current_user_password = logination_form.cleaned_data.get('password')
            current_user: userModel = userModel.objects.filter(
                email__iexact=current_user_email).first()
            if current_user is not None:
                if not current_user.is_active:
                    logination_form.add_error(
                        "email", "حساب کاربری شما فعال نشده است.")
                else:
                    is_password_correct: bool = current_user.check_password(
                        current_user_password)
                    if is_password_correct:
                        login(request=request, user=current_user)
                        return redirect(reverse("user-dashboard"))
                    else:
                        logination_form.add_error(
                            "password", "رمز عبور اشتباه وارد شده است")
            else:
                logination_form.add_error(
                    "email", "شما ابتدا نیاز به ثبت نام در سایت دارید.")

        context = {
            "logination_form": logination_form,
        }
        return render(request, "account_module/login_page.html", context)
        


class logoutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse("login-page"))