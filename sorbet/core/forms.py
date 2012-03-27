from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from urllib2 import urlopen
from bs4 import BeautifulSoup

from .models import Feed

_ = lambda x: x

class FeedForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(FeedForm, self).clean()
        url = cleaned_data.get('url')
        soup = BeautifulSoup(urlopen(url).read())
        if not soup.rss:
            raise forms.ValidationError('Only RSS feeds are currently supported.')

        return cleaned_data


    class Meta:
        model = Feed
        fields = ['url']

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
