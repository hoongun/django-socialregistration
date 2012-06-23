from socialregistration.contrib.facebook.models import FacebookAccessToken
from socialregistration.contrib.facebook.models import FacebookProfile
    
from socialregistration.middleware import SocialMiddleware
    
class FacebookMiddleware(SocialMiddleware):
    class_name = 'Facebook'
    social_name = 'facebook'
    
    def get_uid(self):
        try:
            return FacebookProfile.objects.get(user=self.user).uid
        except FacebookProfile.DoesNotExist:
            return ''
    
    def get_access_token(self):
        try:
            return FacebookAccessToken.objects.get(profile__user=self.user).access_token
        except FacebookAccessToken.DoesNotExist:
            return ''
        
    def get_api(self):
        def wrapped(self):
            if not self.access_token:
                return None
            import facebook
            return facebook.GraphAPI(self.access_token)
        return wrapped