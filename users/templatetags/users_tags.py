from django import template
from catalog.models import Product, Post, Category

register = template.Library()


@register.simple_tag()
def getproductbymeta(http_referer):
    return Product.objects.all().get(slug=http_referer.split('/')[-2]).product_name