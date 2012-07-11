from socialregistration.contrib.vkontakte.models import VkontakteAccessToken
from socialregistration.contrib.vkontakte.models import VkontakteProfile

from socialregistration.middleware import SocialMiddleware

class VkontakteMiddleware(SocialMiddleware):
    class_name = 'Vkontakte'
    social_name = 'vkontakte'
    
    def get_uid(self):
        try:
            return VkontakteProfile.objects.get(user=self.user).vk_uid
        except VkontakteProfile.DoesNotExist:
            return ''
    
    def get_access_token(self):
        try:
            return VkontakteAccessToken.objects.get(profile__user=self.user).access_token
        except VkontakteAccessToken.DoesNotExist:
            return ''
        
    def get_api(self):
        def wrapped(self):
            if not self.access_token:
                return None
            import vkontakte
            return vkontakte.API(token=self.access_token)
        return wrapped