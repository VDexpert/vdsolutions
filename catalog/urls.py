from django.urls import path
from django.views.generic import TemplateView

from catalog.views import*
from catalog.apps import CatalogConfig
from catalog.formset_views import*

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductHomeListView.as_view(), name='home'),
    path('contacts/', ContactsFormView.as_view(), name='contacts'),
    path('category-<str:slug>/', CategoryWithProductsDetailView.as_view(), name='category_with_products'),
    path('category-<str:cat_slug>/<str:prod_slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('create-category/', CategoryCreateView.as_view(), name='create_category'),
    path('update-category/<int:pk>/', CategoryUpdateView.as_view(), name='update_category'),
    path('blog/', PostListView.as_view(), name='post_list'),
    path('blog/<str:slug>/', CategoryWithPostsDetailView.as_view(), name='category_with_posts'),
    path('blog/<str:cat_slug>/<str:post_slug>/', PostDetailView.as_view(), name='post_detail'),
    path('create-post/', PostCreateView.as_view(), name='create_post'),
    path('update-post/<int:pk>/', PostUpdateView.as_view(), name='update_post'),
    path('delete-post/<int:pk>/', PostDeleteView.as_view(), name='delete_post'),
    path('create-product/', ProductCreateWithVersionView.as_view(), name='create_product'),
    path('update-product/<int:pk>/', ProductWithVersionUpdateView.as_view(), name='update_product'),
    path('delete-product/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('page-not-found/', TemplateView.as_view(template_name='catalog/page_404.html'), name='double_404_page'),
    path('thank-for-feedback/', TemplateView.as_view(template_name='catalog/service/after_feedback_page.html'), name='after_feedback'),
    path('thank-for-ordering/', TemplateView.as_view(template_name='catalog/service/after_ordering_page.html'), name='after_ordering'),
    path('update-blog/', ChangeBlogUpdateView.as_view(), name='update_blog'),

]


