from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

class registerForm(forms.Form):
    avatar = forms.ImageField(
        label="عکس پروفایل",
        widget=forms.FileInput(attrs={
                "id":"register_username",
                }),
        error_messages={
            "requird": "پر کردن این فیلد الزامی است",
        }
    )
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(attrs={
                "id":"register_username",
                }),
        error_messages={
            "requird": "پر کردن این فیلد الزامی است",
        }
    )
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(attrs={
                "id":"register_email",
                }),
        validators=[
            validators.EmailValidator(),
            validators.MaxLengthValidator(100),
        ],
        error_messages={
            "requird": "پر کردن این فیلد الزامی است",
        }
    )
    
    password = forms.CharField(
        label="کلمه ی عبور",
        widget=forms.PasswordInput(attrs={
                "id":"register_password",
                }),
        validators=[
            validators.MaxLengthValidator(50),
        ],
    )
    confirm_password = forms.CharField(
        label="تکرار کلمه ی عبور",
        widget=forms.PasswordInput(attrs={
                "id":"register_password_confirm",
                }),
        validators=[
            validators.MaxLengthValidator(50),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if confirm_password == password:
            return confirm_password

        raise ValidationError("کلمه ی عبور و تکرار کلمه ی عبور مغایرت دارند")


class loginForm(forms.Form):
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(attrs={
                "id":"login_email",
                }),
        validators=[
            validators.EmailValidator(),
            validators.MaxLengthValidator(100),
        ],
        error_messages={
            "requird": "پر کردن این فیلد الزامی است",
        }
    )
    
    password = forms.CharField(
        label="کلمه ی عبور",
        widget=forms.PasswordInput(attrs={
                "id":"login_password",
                }),
        validators=[
            validators.MaxLengthValidator(50),
        ],
    )

