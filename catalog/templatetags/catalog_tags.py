from django import template
from catalog.auxfunc import translit
from catalog.models import Version, Contacts
import re

register = template.Library()


@register.simple_tag()
def mediapath(picture):
    return f'/media/{picture}'


@register.simple_tag()
def translittag(text):
    return translit.do(str(text))


@register.simple_tag()
def getversion(product):
    version = ' '.join(re.findall(r'{([^<>]+)}', str(Version.objects.all().filter(product=product, status='активно').values('description')))).replace('description', '').replace("'", '').replace(':', '')
    if version:
        version = version[:99] + '...' if len(version) >= 100 else version
        return 'Версия:' + version
    else:
        return ''


@register.simple_tag()
def getusername(email):
    return email.split('@')[0]

@register.simple_tag()
def cleanversionerror(error):
    return str(error).replace("'", '').replace('{', '').replace('}', '').replace(':', '').replace('[', '').replace(']', '').replace('value', '')


@register.simple_tag()
def getemail():
    return Contacts.objects.first().email


@register.simple_tag()
def getphone():
    return Contacts.objects.first().phone