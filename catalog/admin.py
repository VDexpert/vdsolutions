from django.contrib import admin
from catalog.models import*

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'slug', 'unit_price', 'category')
    search_fields = ('product_name', 'description')
    list_filter = ('category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    prepopulated_fields = {'slug': ('category_name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'create_at', 'change_at', 'count_views', 'status')
    search_fields = ('title', 'content')
    list_filter = ('category',)


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('home_h1', 'home_annotation', 'title')

    def has_add_permission(self, request):
        if Home.objects.all().filter(id=1).exists():
            return False

        return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Blog)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('blog_h1', 'blog_annotation', 'title')

    def has_add_permission(self, request):
        if Blog.objects.all().filter(id=1).exists():
            return False

        return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('official_company_name', 'itin', 'phone', 'email', 'address')

    def has_add_permission(self, request):
        if Contacts.objects.all().filter(id=1).exists():
            return False

        return True

    def has_delete_permission(self, request, obj=None):
        return False