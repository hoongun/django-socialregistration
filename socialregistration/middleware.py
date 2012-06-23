import warnings
from django.utils.functional import SimpleLazyObject

#from socialregistration.contrib.facebook.middleware import FacebookMiddleware


#warnings.warn("'socialregistration.middleware.FacebookMiddleware' will be removed. "
#    "Use 'socialregistration.contrib.facebook.middleware.FacebookMiddleware' instead.")



class SocialMiddleware(object):
    class_name = ''
    social_name = ''
    
    user = None
    
    def get_object(self):
        def wrapped():
            return type(self.class_name, (object,), {'uid': self.get_uid(), 
                                                'access_token': self.get_access_token(), 
                                                'api': self.get_api()})()    
        return wrapped
    
    
    def process_request(self, request):
        """
        Enables ``request.social`` in your views for authenticated users.
        It's a lazy object that does database lookups.
        """
        self.user = request.user
        setattr(request, self.social_name, SimpleLazyObject(self.get_object()))
        return None