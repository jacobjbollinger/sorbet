from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'', include('sorbet.core.urls', namespace='core')),
    url(r'^feeds/', include('sorbet.feedmanager.urls', namespace='feedmanager')),
)
