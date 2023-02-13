from django.contrib.sitemaps import Sitemap
from catalog.models import*

class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.all().filter(status=Product.STATUS_ACTIVE, banned='одобрено модератором')

    def lastmod(self, obj):
        return obj.change_at


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return [x for x in Category.objects.all() if Product.objects.all().filter(category=x).exists()]

    def lastmod(self, obj):
        return obj.add_new_prod


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Post.objects.all().filter(status=Product.STATUS_ACTIVE, banned='одобрено модератором')

    def lastmod(self, obj):
        return obj.change_at