from django import template

from socialregistration.templatetags import button

register = template.Library()

register.tag('vkontakte_button', button('socialregistration/vkontakte/vkontakte_button.html'))