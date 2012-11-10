from django.conf import settings
from django.utils.functional import SimpleLazyObject

from socialregistration.contrib.twitter.models import TwitterAccessToken
from socialregistration.contrib.twitter.models import TwitterProfile


KEY = getattr(settings, 'TWITTER_CONSUMER_KEY', '')
SECRET_KEY = getattr(settings, 'TWITTER_CONSUMER_SECRET_KEY', '')


def get_uid(user):
    try:
        return TwitterProfile.objects.get(user=user).twitter_id
    except TwitterProfile.DoesNotExist:
        return ''


def get_access_token(user):
    try:
        token = TwitterAccessToken.objects.get(profile__user=user)
        return (token.oauth_token, token.oauth_token_secret)
    except TwitterAccessToken.DoesNotExist:
        return ''


def get_api():
    def wrapped(self):
        if not self.access_token:
            return None
        
        import tweepy
        oauth_token, oauth_token_secret = self.access_token
        auth = tweepy.OAuthHandler(KEY, SECRET_KEY)
        auth.set_access_token(oauth_token, oauth_token_secret)
        return tweepy.API(auth)
    return wrapped


def get_object(user):
    def wrapped():
        return type('Twitter', (object,), {'uid': get_uid(user),
                                            'access_token': get_access_token(user),
                                            'get_api': get_api()})()
    return wrapped


class TwitterMiddleware(object):
    class_name = 'Twitter'
    social_name = 'twitter'

    def process_request(self, request):
        """
        Enables ``request.social`` in your views for authenticated users.
        It's a lazy object that does database lookups.
        """
        self.user = request.user
        setattr(request, self.social_name, SimpleLazyObject(get_object(self.user)))
        return None
