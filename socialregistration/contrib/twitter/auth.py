from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.sites.models import Site
from socialregistration.contrib.twitter.models import TwitterProfile


class TwitterAuth(ModelBackend):
    GET_FIRST_RECIEVED_USER = getattr(settings, 'GET_FIRST_RECIEVED_USER', True)
    
    def authenticate(self, twitter_id = None):
        site = Site.objects.get_current()
        try:
            if self.GET_FIRST_RECIEVED_USER:
                return TwitterProfile.objects.filter(
                    twitter_id = twitter_id,
                    site = site)[0].user
            return TwitterProfile.objects.get(
                twitter_id = twitter_id,
                site = site).user
        except TwitterProfile.DoesNotExist:
            return None
