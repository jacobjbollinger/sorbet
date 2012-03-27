from django.conf.urls import patterns, url


urlpatterns = patterns('sorbet.core.views',
    url(r'^$', 'home', name='home'),
    url(r'^register/$', 'register', name='register'),
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^panel/$', 'panel', name='panel'),
)
