from django.contrib.auth.backends import ModelBackend
from django.contrib.sites.models import Site
from socialregistration.contrib.vkontakte.models import VkontakteProfile


class VkontakteAuth(ModelBackend):
    supports_object_permissions = False
    supports_anonymous_user = False
    
    def authenticate(self, uid = None):
        try:
            return VkontakteProfile.objects.get(
                uid = uid,
                site = Site.objects.get_current()).user
        except VkontakteProfile.DoesNotExist:
            return None
