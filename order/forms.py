from django import forms

from .models import RequestedProduct, Prescription


class RequestProductForm(forms.ModelForm):
    class Meta:
        model = RequestedProduct
        exclude = ['user', 'status', 'note']


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        exclude = ['user', 'height', 'width']
