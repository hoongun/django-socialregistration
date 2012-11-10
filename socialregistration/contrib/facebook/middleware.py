from django.utils.functional import SimpleLazyObject

from socialregistration.contrib.facebook.models import FacebookAccessToken
from socialregistration.contrib.facebook.models import FacebookProfile


def get_uid(user):
    try:
        return FacebookProfile.objects.get(user=user).uid
    except FacebookProfile.DoesNotExist:
        return ''


def get_access_token(user):
    try:
        return FacebookAccessToken.objects.get(profile__user=user).access_token
    except FacebookAccessToken.DoesNotExist:
        return ''


def get_api():
    def wrapped(self):
        if not self.access_token:
            return None
        import facebook
        return facebook.GraphAPI(self.access_token)
    return wrapped


def get_object(user):
    def wrapped():
        return type('Facebook', (object,), {'uid': get_uid(user),
                                            'access_token': get_access_token(user),
                                            'get_api': get_api()})()
    return wrapped


class FacebookMiddleware(object):
    class_name = 'Facebook'
    social_name = 'facebook'

    def process_request(self, request):
        """
        Enables ``request.social`` in your views for authenticated users.
        It's a lazy object that does database lookups.
        """
        self.user = request.user
        setattr(request, self.social_name, SimpleLazyObject(get_object(self.user)))
        return None
