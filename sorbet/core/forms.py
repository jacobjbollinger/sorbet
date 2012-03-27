from django import forms

from urllib2 import urlopen
from bs4 import BeautifulSoup

from .models import Feed


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
            user = User.objects.get(email=username)
            if user.get_profile().invited:
                return username
        except User.DoesNotExist:
            pass

        raise forms.ValidationError("You haven't been invited yet.")

    def clean(self):
        return super(EmailUserCreationForm, self).clean()
