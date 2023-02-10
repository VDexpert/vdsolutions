from django.contrib import admin
from catalog.models import*

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'slug', 'unit_price', 'category')
    search_fields = ('product_name', 'description')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('product_name',)} #TODO: разобраться, почему не работает


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    prepopulated_fields = {'slug': ('category_name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'create_at', 'change_at', 'count_views', 'status')
    search_fields = ('title', 'content')
