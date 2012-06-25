import warnings

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.sites.models import Site
from socialregistration.contrib.twitter.models import TwitterProfile


class TwitterAuth(ModelBackend):

    def authenticate(self, twitter_id = None):
        site = Site.objects.get_current()
        profiles = TwitterProfile.objects.filter(twitter_id=twitter_id, site=site)
        count = profiles.count()
        if count == 0:
            return None
        elif count != 1 or not getattr(settings, 'GET_FIRST_RECIEVED_USER', True):
            warnings.warn('More than one profile for user')
        return profiles[0].user