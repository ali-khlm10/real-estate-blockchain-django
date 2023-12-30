from django import forms


class increaseUserInventoryForm(forms.Form):
    user_inventory = forms.CharField(
        label="افزایش موجودی حساب ",
        widget=forms.NumberInput(attrs={
            "id": "user_invetory_input_number",
        }),
        error_messages={
            "requird": "پر کردن این فیلد الزامی است",
        }
    )
