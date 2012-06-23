from django.conf import settings
from django.conf.urls.defaults import *
from socialregistration.contrib.vkontakte.views import VkontakteSetup, \
    VkontakteRedirect, VkontakteCallback
 
urlpatterns = patterns('',
    url('^redirect/$', VkontakteRedirect.as_view(), name='redirect'),
    url('^callback/$', VkontakteCallback.as_view(), name='callback'),
    url('^setup/$', VkontakteSetup.as_view(), name='setup'),
)
