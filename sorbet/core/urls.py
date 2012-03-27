from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'sorbet.core.views.home', name='home'),
    url(r'^accounts/register/$', 'sorbet.core.views.register', name='register'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'core/login.html'}, name='login'),
    url(r'^accounts/logout/$', 'sorbet.core.views.logout_user', name='logout'),
    url(r'^feeds/$', 'sorbet.core.views.feeds', name='feeds'),
    url(r'^featured/$', 'sorbet.core.views.featured', name='featured'),
)
