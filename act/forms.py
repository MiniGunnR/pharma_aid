from django.forms import ModelForm
from django import forms

from act.models import Address, AddressInfo, User


class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ['user', 'default']


class AddressInfoForm(ModelForm):
    class Meta:
        model = AddressInfo
        exclude = ['address']


class AddMobileForm(forms.Form):
    mobile = forms.CharField(max_length=50)

