from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

class registerForm(forms.Form):
    avatar = forms.FileField(
        label="آواتار",
        widget=forms.FileInput(),
        error_messages={
            "requird": "پر کردن این فیلد الزامی است",
        }
    )
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(),
        error_messages={
            "requird": "پر کردن این فیلد الزامی است",
        }
    )
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(),
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
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(50),
        ],
    )
    confirm_password = forms.CharField(
        label="تکرار کلمه ی عبور",
        widget=forms.PasswordInput(),
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
