from django.urls import path
from django.views.generic import TemplateView
from users.views import*
from users.apps import UsersConfig


app_name = UsersConfig.name

urlpatterns = [
    path('products/', ProductUserListView.as_view(), name='user_products'),
    path('posts/', PostUserListView.as_view(), name='user_posts'),
    path('categories/', CategoryUserListView.as_view(), name='categories_for_content_manager'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('confirm-email/', ConfirmEmailTemplateView.as_view(), name='confirm_email'),
    path('verify-email/<uidb64>/<token>/', EmailVerifyView.as_view(), name='verify_email'),
    path('invalid-verify/', InvalidVerifyTemplateView.as_view(), name='invalid_verify'),
    path('registration/', RegisterUser.as_view(), name='register'),
    path('edit-profile/', UserUpdateProfileView.as_view(), name='edit_profile'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('reset-password/', CustomPasswordResetFormView.as_view(), name='reset_password'),
    path('reset-password-confirm/', ConfirmResetPasswordTemplateView.as_view(), name='confirm_reset'),
    path('error-access/', ErrorPermissionTemplateView.as_view(), name='error_permission'),
    path('update-ban-status-product/<int:pk>/', ChangeProductBannedFormView.as_view(), name='product-ban'),
    path('update-ban-status-post/<int:pk>/', ChangePostBannedFormView.as_view(), name='post-ban'),
    path('some-error/', TemplateView.as_view(template_name='users/some_error.html'), name='some-error'),

]


