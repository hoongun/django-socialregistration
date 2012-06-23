from django.conf import settings

from socialregistration.contrib.twitter.models import TwitterAccessToken
from socialregistration.contrib.twitter.models import TwitterProfile
from socialregistration.middleware import SocialMiddleware


KEY = getattr(settings, 'TWITTER_CONSUMER_KEY', '')
SECRET_KEY = getattr(settings, 'TWITTER_CONSUMER_SECRET_KEY', '')

class TwitterMiddleware(SocialMiddleware):
    class_name = 'Twitter'
    social_name = 'twitter'

    
    def get_uid(self):
        try:
            return TwitterProfile.objects.get(user=self.user).twitter_id
        except TwitterProfile.DoesNotExist:
            return ''
    
    def get_access_token(self):
        try:
            token = TwitterAccessToken.objects.get(profile__user=self.user)
            return (token.oauth_token, token.oauth_token_secret)
        except TwitterAccessToken.DoesNotExist:
            return ''
        
    def get_api(self):
        def wrapped(self):
            if not self.access_token:
                return None
            
            import tweepy
            oauth_token, oauth_token_secret = self.access_token
            auth = tweepy.OAuthHandler(KEY, SECRET_KEY)
            auth.set_access_token(oauth_token, oauth_token_secret)
            return tweepy.API(auth)
        return wrapped
