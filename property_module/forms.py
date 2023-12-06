from django import forms


class propertyForm(forms.Form):
    type = forms.CharField(
        label="نوع ملک",
        widget=forms.TextInput(attrs={
            "id": "property_type",
        }),
        error_messages={
            "requird": "پر کردن این فیلد الزامی است",
        }
    )
    title = forms.CharField(
        label="عنوان ملک",
        widget=forms.TextInput(attrs={
            "id": "property_title",
        }),
        error_messages={
            "requird": "پر کردن این فیلد الزامی است",
        }
    )

    price = forms.CharField(
        label="قیمت ملک",
        widget=forms.NumberInput(attrs={
            "id": "property_price",
        }),
        error_messages={
            "requird": "پر کردن این فیلد الزامی است",
        }
    )

    length = forms.CharField(
        label="متراژ ملک",
        widget=forms.NumberInput(attrs={
            "id": "property_length",
        }),
        error_messages={
            "requird": "پر کردن این فیلد الزامی است",
        }
    )

    image = forms.ImageField(
        label="تصویر ملک",
        widget=forms.FileInput(attrs={
            "id": "property_image",
        }),
        error_messages={
            "requird": "پر کردن این فیلد الزامی است",
        }
    )

    short_description = forms.CharField(
        label="توضیحات کوتاه",
        widget=forms.TextInput(attrs={
            "id": "property_short_description",
        }),
        error_messages={
            "requird": "پر کردن این فیلد الزامی است",
        }
    )

    description = forms.Field(
        label="توضیحات کامل ملک",
        widget=forms.Textarea(attrs={
            "id": "property_description",
            "cols": "30",
            "rows": "12",
        }),
        error_messages={
            "requird": "پر کردن این فیلد الزامی است",
        }
    )

    address = forms.Field(
        label="آدرس ملک",
        widget=forms.Textarea(attrs={
            "id": "property_address",
            "cols": "30",
            "rows": "8",
        }),
        error_messages={
            "requird": "پر کردن این فیلد الزامی است",
        }
    )

