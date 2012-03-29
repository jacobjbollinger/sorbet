from django import forms

from urllib2 import urlopen
from bs4 import BeautifulSoup

from .models import Feed


class FeedForm(forms.ModelForm):
    def clean_url(self):
        url = self.cleaned_data['url']
        soup = BeautifulSoup(urlopen(url).read())
        if not soup.rss:
            raise forms.ValidationError('Only RSS feeds are currently supported.')
        return url

    class Meta:
        model = Feed
        fields = ['url']