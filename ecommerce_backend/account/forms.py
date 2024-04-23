from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django import forms

from .models import User, Address


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'avatar')


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('receiver', 'country', 'city', 'street', 'province', 'zip_code', 'phone', 'is_default')