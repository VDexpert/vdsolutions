from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from catalog.models import Product, Post, Category

register = template.Library()


@register.filter(needs_autoescape=False)
def checkexistproduct(category, autoescape=True):

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    return True if Product.objects.all().filter(category=category).exists() else False


@register.filter(needs_autoescape=False)
def checkexistpost(category, autoescape=True):

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    return True if Post.objects.all().filter(category=category).exists() else False

@register.filter(needs_autoescape=True)
def getemptyfields(category, autoescape=True):

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    return [mark_safe(esc(field.verbose_name)) for field in category._meta.fields if not category.__getattribute__(str(field).split('.')[-1].replace("'", ''))]


@register.filter(needs_autoescape=False)
def cutbrackets(categories, autoescape=False):

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    return str(categories).replace(']', '').replace('[', '')


@register.filter(needs_autoescape=False)
def customtruncatechars(content, autoescape=False):

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    return mark_safe(esc(content[:200] + '...'))