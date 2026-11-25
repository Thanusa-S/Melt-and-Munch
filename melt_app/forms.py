from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)
from django.contrib.auth.models import User
from .models import *


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "email",
            "password1",
            "password2",
        ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Enter username",
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter password",
        })
    )



class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Order

        fields = [
            "full_name",
            "email",
            "phone",
            "address",
            "city",
            "postal_code",
        ]

        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your full name"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your email address"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your phone number"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter your delivery address"
            }),

            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your city"
            }),

            "postal_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter postal code"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["address"].required = False
        self.fields["city"].required = False
        self.fields["postal_code"].required = False



class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }

from django import forms
from .models import IceCream


class IceCreamSearchForm(forms.Form):

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search your favourite flavour...',
            'class': 'ice-search-input'
        })
    )

    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Flavours')] + IceCream.CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'ice-filter-select'
        })
    )

    sort = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Recommended'),
            ('price_low', 'Price: Low to High'),
            ('price_high', 'Price: High to Low'),
            ('name', 'Name: A to Z'),
        ],
        widget=forms.Select(attrs={
            'class': 'ice-filter-select'
        })
    )


class IceCreamForm(forms.ModelForm):

    class Meta:
        model = IceCream

        fields = [
            'name',
            'category',
            'description',
            'price',
            'image',
            'is_available',
            'is_featured',
            'stock_quantity',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ice cream name',
            }),

            'category': forms.Select(attrs={
                'class': 'form-control',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe this flavour...',
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),

            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name", "description", "price",
            "image", "category", "is_featured", "is_available",
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]