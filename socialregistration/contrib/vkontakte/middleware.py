from django.utils.functional import SimpleLazyObject

from socialregistration.contrib.vkontakte.models import VkontakteAccessToken
from socialregistration.contrib.vkontakte.models import VkontakteProfile


def get_uid(user):
    try:
        return VkontakteProfile.objects.get(user=user).vk_uid
    except VkontakteProfile.DoesNotExist:
        return ''


def get_access_token(user):
    try:
        return VkontakteAccessToken.objects.get(profile__user=user).access_token
    except VkontakteAccessToken.DoesNotExist:
        return ''


def get_api():
    def wrapped(self):
        if not self.access_token:
            return None
        import vkontakte
        return vkontakte.API(token=self.access_token)
    return wrapped


def get_object(user):
    def wrapped():
        return type('Vkontakte', (object,), {'uid': get_uid(user),
                                            'access_token': get_access_token(user),
                                            'get_api': get_api()})()
    return wrapped


class VkontakteMiddleware(object):
    class_name = 'Vkontakte'
    social_name = 'vkontakte'

    def process_request(self, request):
        """
        Enables ``request.social`` in your views for authenticated users.
        It's a lazy object that does database lookups.
        """
        self.user = request.user
        setattr(request, self.social_name, SimpleLazyObject(get_object(self.user)))
        return None
