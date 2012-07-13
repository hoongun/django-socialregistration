import warnings

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.sites.models import Site
from socialregistration.contrib.facebook.models import FacebookProfile


class FacebookAuth(ModelBackend):
    supports_object_permissions = False
    supports_anonymous_user = False
    
    def authenticate(self, uid = None):
        site = Site.objects.get_current()
        profiles = FacebookProfile.objects.filter(uid=uid, site=site)
        count = profiles.count()
        if count == 0:
            return None
        elif count != 1 or not getattr(settings, 'GET_FIRST_RECIEVED_USER', True):
            warnings.warn('More than one profile for user')
        return profiles[0].user