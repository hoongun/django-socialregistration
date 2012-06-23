from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.sites.models import Site
from socialregistration.contrib.vkontakte.models import VkontakteProfile


class VkontakteAuth(ModelBackend):
    supports_object_permissions = False
    supports_anonymous_user = False
    GET_FIRST_RECIEVED_USER = getattr(settings, 'GET_FIRST_RECIEVED_USER', True)
    
    def authenticate(self, uid = None):
        site = Site.objects.get_current()
        try:
            if self.GET_FIRST_RECIEVED_USER:
                return VkontakteProfile.objects.filter(
                    uid = uid,
                    site = site)[0].user
            return VkontakteProfile.objects.get(
                uid = uid,
                site = site).user
        except VkontakteProfile.DoesNotExist:
            return None
