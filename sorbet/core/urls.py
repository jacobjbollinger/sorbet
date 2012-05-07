from django.conf.urls import patterns, url

from sorbet.core.forms import EmailAuthenticationForm


urlpatterns = patterns('',
    url(r'^$', 'sorbet.core.views.home', name='home'),
    url(r'^accounts/invite/$', 'sorbet.core.views.invite', name='invite'),
    url(r'^accounts/register/$', 'sorbet.core.views.register', name='register'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'core/login.html',
         'authentication_form': EmailAuthenticationForm}, name='login'),
    url(r'^accounts/logout/$', 'sorbet.core.views.logout_user', name='logout'),
)
