from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


_ = lambda x: x


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label=_("E-mail"), max_length=75)


class EmailUserCreationForm(UserCreationForm):
    username = forms.EmailField(label=_("E-mail"), max_length=75)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(email=username)
        except User.DoesNotExist:
            return username

    def clean(self):
        return super(EmailUserCreationForm, self).clean()
