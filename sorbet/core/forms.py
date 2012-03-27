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
