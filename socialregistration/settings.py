from django.conf import settings

SESSION_KEY = getattr(settings, 'SOCIALREGISTRATION_SESSION_KEY', 'socialreg:')
PROFILES = {
    'facebook': 'FacebookProfile',
    'foursquare': 'FoursquareProfile',
    'github': 'GithubProfile',
    'linkedin': 'LinkedInProfile',
    'openid': 'OpenIDProfile',
    'tumblr': 'TumblrProfile',
    'twitter': 'TwitterProfile',
    'vkontakte': 'VkontakteProfile',
}