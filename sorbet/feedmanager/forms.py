from django import forms

from urllib2 import urlopen
from bs4 import BeautifulSoup
from re import search

from .models import Feed


class FeedForm(forms.ModelForm):
    def clean_url(self):
        url = self.cleaned_data['url']

        # For people who don't add the http, urlopen bugs out without this.
        if not search('^http', url): url = ''.join(['http://', url])

        xml = urlopen(url).read()
        soup = BeautifulSoup(xml)

        if not soup.rss and not soup.feed:
            raise forms.ValidationError('Only RSS and ATOM URLs/feeds are currently supported.')

        return url

    class Meta:
        model = Feed
        fields = ['url']
