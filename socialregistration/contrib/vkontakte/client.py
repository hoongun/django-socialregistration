from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
from socialregistration.clients.oauth import OAuth2, OAuthError
from socialregistration.settings import SESSION_KEY
import json
import vkontakte

class Vkontakte(OAuth2):
    client_id = getattr(settings, 'VKONTAKTE_APP_ID', '')
    secret = getattr(settings, 'VKONTAKTE_SECRET_KEY', '')
    scope = getattr(settings, 'VKONTAKTE_REQUEST_PERMISSIONS', '')
    
    auth_url = 'http://oauth.vk.com/authorize'
    access_token_url = 'https://oauth.vk.com/access_token'
    
    #api = None
    _user_id = None
    _user_info = None
    
    
    def request_access_token(self, params):
        """
        Request the access token from `self.access_token_url`. The default 
        behaviour is to use a `POST` request, but some services use `GET` 
        requests. Individual clients can override this method to use the 
        correct HTTP method.
        """
        return self.request(self.access_token_url, method="GET", params=params,
            is_signed=False)
    

    def _get_access_token(self, code, **params):
        """
        Fetch an access token with the provided `code`.
        """
        params.update({
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.secret,
            'redirect_uri': self.get_callback_url(),
        })
        
        resp, content = self.request_access_token(params=params)
        print 'Response content ', resp, content 
        import ast
        content = ast.literal_eval(content)
        print 'OAuth content dict = ', content
        #content = smart_unicode(content)
        #content = self.parse_access_token(content)
        self._user_id = content['user_id']
        
        if 'error' in content:
            raise OAuthError(_(
                u"Received error while obtaining access token from %s: %s") % (
                    self.access_token_url, content['error']))

        return content

    def get_callback_url(self):
        if self.is_https():
            return 'https://%s%s' % (Site.objects.get_current().domain,
                reverse('socialregistration:vkontakte:callback'))
        return 'http://%s%s' % (Site.objects.get_current().domain,
            reverse('socialregistration:vkontakte:callback'))

    def get_user_info(self):
        if self._user_info is None and self._user_id is not None:
            api = vkontakte.API(token=self._access_token)
            self._user_info = api.get('users.get', uids=self._user_id, fields='uid, first_name, '\
                                           'last_name, nickname, screen_name, sex, bdate (birthdate), '\
                                           'city, country, timezone, photo, photo_medium, photo_big, '\
                                           'has_mobile, rate, contacts, education, online, counters')[0]
        return self._user_info
    
    @staticmethod
    def get_session_key():
        return '%svkontakte' % SESSION_KEY
