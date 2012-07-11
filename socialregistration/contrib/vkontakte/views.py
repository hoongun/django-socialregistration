from django.core.urlresolvers import reverse
from socialregistration.contrib.vkontakte.client import Vkontakte
from socialregistration.contrib.vkontakte.models import VkontakteProfile
from socialregistration.views import OAuthRedirect, OAuthCallback, SetupCallback

class VkontakteRedirect(OAuthRedirect):
    client = Vkontakte
    template_name = 'socialregistration/vkontakte/vkontakte.html'

class VkontakteCallback(OAuthCallback):
    client = Vkontakte
    template_name = 'socialregistration/vkontakte/vkontakte.html'
    
    def get_redirect(self):
        return reverse('socialregistration:vkontakte:setup')

class VkontakteSetup(SetupCallback):
    client = Vkontakte
    profile = VkontakteProfile
    template_name = 'socialregistration/vkontakte/vkontakte.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'vk_uid': client.get_user_info()['uid']}
