from django import forms
from act.models import User

from allauth.account.forms import LoginForm
from pharma_aid import settings


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    mobile = forms.CharField(max_length=30, label='Mobile Number', widget=forms.TextInput(attrs={'placeholder': 'Mobile Number'}))
    institution = forms.CharField(max_length=100, required=False)
    department = forms.CharField(max_length=100, required=False)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.mobile = self.cleaned_data['mobile']
        user.save()
        # user.profile.user = user
        # user.profile.institution = self.cleaned_data['institution']
        # user.profile.department = self.cleaned_data['department']
        # user.profile.save()


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if settings.ACCOUNT_AUTHENTICATION_METHOD == "email":
            login_widget = forms.TextInput(attrs={'type': 'text',
                                                  'placeholder':
                                                  ('Email or Mobile'),
                                                  'autofocus': 'autofocus'})
            login_field = forms.CharField(label=("Email or Mobile"),
                                           widget=login_widget)
        self.fields["login"] = login_field
        set_form_field_order(self,  ["login", "password", "remember"])

    def user_credentials(self):
        credentials = {}
        uid = self.cleaned_data["login"]
        if '@' in uid and '.' in uid:
            login = uid
        else:
            login = User.objects.filter(mobile=uid).values('email')[0]['email']
        if settings.ACCOUNT_AUTHENTICATION_METHOD == "email":
            credentials["email"] = login
        credentials["password"] = self.cleaned_data["password"]
        return credentials

# this is to set the form field in order
def set_form_field_order(form, fields_order):
    if hasattr(form.fields, 'keyOrder'):
        form.fields.keyOrder = fields_order
    else:
        # Python 2.7+
        from collections import OrderedDict
        assert isinstance(form.fields, OrderedDict)
        form.fields = OrderedDict((f, form.fields[f])
                                  for f in fields_order)
