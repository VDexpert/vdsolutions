from django import template
from catalog.auxfunc import translit
from catalog.models import Version, Contacts, Home
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
    return str(error).lower().replace("'", '').replace('{', '').replace('}', '').replace(':', '').replace('[', '').replace(']', '').replace('value', '').replace(',', '').replace('description', '''"Улучшения" - ''')


@register.simple_tag()
def getemail():
    if Contacts.objects.all():
        return Contacts.objects.all().first().email

    return 'False email'


@register.simple_tag()
def getphone():
    if Contacts.objects.all():
        return Contacts.objects.all().first().phone

    return 'False phone'


@register.simple_tag()
def getyandexcounter():
    if Home.objects.all().first():
        if Home.objects.all().first().yandex_counter:
            return Home.objects.all().first().yandex_counter
        else:
            return ""

    return ""


@register.simple_tag()
def getgooglecounter():
    if Home.objects.all().first():
        if Home.objects.all().first().google_counter:
            return Home.objects.all().first().google_counter
        else:
            return ""

    return ""