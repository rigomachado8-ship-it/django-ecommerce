from django import forms


class RegisterForm(forms.Form):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('vendor', 'Vendor'),
    )

    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


from django import forms
from .models import Store, Product


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'address']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image']

from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)   

from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'address', 'city', 'postal_code'] 