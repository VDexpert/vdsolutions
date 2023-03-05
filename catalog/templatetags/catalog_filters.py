from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from catalog.models import Version, Category, Product
import re

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def mediapath(picture, autoescape=True):

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    result = f'/media/{esc(picture)}'
    return mark_safe(result)


@register.filter(needs_autoescape=False)
def getusergroup(user, autoescape=False):

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    return user.groups.filter(name='Контент-менеджеры').exists()


@register.filter(needs_autoescape=False)
def getcategories(user, autoescape=False):

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    return [x for x in Category.objects.all() if Product.objects.all().filter(status=Product.STATUS_ACTIVE, banned=Product.BANNED_FALSE, category=x).first()]


@register.filter()
def checkurlpath(path, name_filter):
    return True if re.findall(name_filter, path) else False