from django.conf.urls import patterns, url


urlpatterns = patterns('sorbet.feedmanager.views',
    url(r'^featured/$', 'featured', name='featured'),
    url(r'^$', 'feeds', name='feeds'),
    url(r'^add-feed/$', 'add_feed', name='add-feed'),
    url(r'^remove-feed/(?P<feed_id>\d*)$', 'remove_feed', name='remove-feed'),
)
