from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.sites.models import Site
from django.db import models
from socialregistration.signals import connect, login

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class VkontakteProfile(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    vk_uid = models.CharField(max_length=255, blank=False, null=False)

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.vk_uid)
        except models.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(vk_uid=self.vk_uid)


class VkontakteAccessToken(models.Model):
    profile = models.OneToOneField(VkontakteProfile, related_name='access_token')
    access_token = models.CharField(max_length=255)


def save_vkontakte_token(sender, user, profile, client, **kwargs):
    try:
        VkontakteAccessToken.objects.get(profile=profile).delete()
    except VkontakteAccessToken.DoesNotExist:
        pass

    VkontakteAccessToken.objects.create(profile=profile,
        access_token=client._access_token)

connect.connect(save_vkontakte_token, sender=VkontakteProfile,
    dispatch_uid='socialregistration.vkontakte.connect')
login.connect(save_vkontakte_token, sender=VkontakteProfile,
    dispatch_uid='socialregistration.vkontakte.login')
