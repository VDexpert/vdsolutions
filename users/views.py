import os
from django.contrib.auth import login, logout, authenticate, models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView, CreateView, ListView, FormView, TemplateView
from catalog.forms import ProductBannedForm, PostBannedForm
from catalog.models import Product, Post, Category
from users.models import User
from users.forms import CustomUserEditForm, RegisterUserForm, CustomAuthenticationForm, CustomPasswordResetForm
from users.utils import send_email_for_verify, send_email_for_reset
from django.contrib.auth.tokens import default_token_generator as token_generator

PermissionsMixin


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/registration.html'
    c = 'catalog'
    get_perm = models.Permission.objects.get_by_natural_key

    user_permissions = [
        {'app': c, 'act': 'add_product', 'mod': 'product'}, {'app': c, 'act': 'change_product', 'mod': 'product'},
        {'app': c, 'act': 'view_product', 'mod': 'product'}, {'app': c, 'act': 'delete_product', 'mod': 'product'},
        {'app': c, 'act': 'add_post', 'mod': 'post'}, {'app': c, 'act': 'change_post', 'mod': 'post'},
        {'app': c, 'act': 'delete_post', 'mod': 'post'}, {'app': c, 'act': 'view_post', 'mod': 'post'},
        {'app': c, 'act': 'view_category', 'mod': 'category'}
    ]
    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)

        if self.request.user.is_authenticated:
            return redirect('users:user_products')

        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            try:
                send_email_for_verify(request, user)

                for perm in self.user_permissions:
                    user.user_permissions.add(self.get_perm(codename=perm['act'], app_label=perm['app'], model=perm['mod']).pk)

            except Exception as e:
                os.system(f'echo {e} >> register_errors.txt')
                return redirect('users:some-error')

            else:
                return redirect('users:confirm_email')

        context = {'form': form}

        return render(request, self.template_name, context)


class LoginUser(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.has_perm('catalog.management_posts') or user.has_perm('catalog.management_category'):
            return reverse_lazy('users:user_posts')

        return reverse_lazy('users:user_products')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        if self.request.user.is_authenticated:
            return redirect('users:user_products')

        return self.render_to_response(self.get_context_data())


class EmailVerifyView(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)

            return redirect('users:user_products')

        return redirect('users:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None

        return user


def logout_user(request):
    logout(request)

    return redirect('users:login')


class UserUpdateProfileView(UpdateView):
    model = User
    form_class = CustomUserEditForm
    template_name = 'users/edit_profile.html'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        if not self.request.user.is_authenticated:
            return redirect('users:login')

        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:user_products')


class ProductUserListView(ListView):
    model = Product
    template_name = 'users/product_list_profile.html'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user = self.request.user

        if not self.request.user.is_authenticated:
            return redirect('users:login')

        if user.has_perm('catalog.moderating_products'):
            return self.render_to_response(self.get_context_data())

        if user.has_perm('catalog.management_category') or user.has_perm('catalog.management_posts'):
            return redirect('users:error_permission')

        return self.render_to_response(self.get_context_data())


    def get_queryset(self):
        user = self.request.user

        if user.has_perm('catalog.moderating_products'):
            return super().get_queryset()

        return super().get_queryset().filter(user=self.request.user)


class PostUserListView(ListView):
    model = Post
    template_name = 'users/post_list_profile.html'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user = self.request.user

        if not user.is_authenticated:
            return redirect('users:login')

        if user.has_perm('catalog.moderating_products'):
            return redirect('users:error_permission')

        if user.has_perm('catalog.management_posts') or user.has_perm('catalog.management_category'):
            return self.render_to_response(self.get_context_data())

        if not user.has_perm('catalog.view_post'):
            return redirect('users:error_permission')

        return self.render_to_response(self.get_context_data())

    def get_queryset(self):
        user = self.request.user

        if user.has_perm('catalog.management_posts')or user.has_perm('catalog.management_category'):
            return super().get_queryset()

        return super().get_queryset().filter(user=self.request.user)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/change_password.html'
    model = User
    success_url = reverse_lazy('users:user_products')


class CustomPasswordResetFormView(FormView):
    template_name = 'users/reset_password_form.html'
    form_class = CustomPasswordResetForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        if self.request.user.is_authenticated:
            return redirect('users:user_products')

        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        return reverse_lazy('users:confirm_reset')

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.all().get(email=email)
            new_password = User.objects.make_random_password(length=20)
            user.set_password(new_password)
            user.save()

            domain = get_current_site(self.request)

            send_email_for_reset(domain, email, new_password)

            return redirect('users:confirm_reset')

        context = {'form': form}

        return render(request, self.template_name, context)


class ConfirmEmailTemplateView(TemplateView):
    template_name ='users/confirm_email.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            return redirect('users:user_products')

        return self.render_to_response(context)


class ConfirmResetPasswordTemplateView(TemplateView):
    template_name ='users/reset_password_confirm.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            return redirect('users:user_products')

        return self.render_to_response(context)


class InvalidVerifyTemplateView(TemplateView):
    template_name = 'users/invalid_verify.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            return redirect('users:user_products')

        return self.render_to_response(context)


class MenuProfileTemplateView(TemplateView):
    template_name = 'users/includes/menu_profile.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ChangeProductBannedFormView(UpdateView):
    model = Product
    form_class = ProductBannedForm
    template_name = 'users/product_banned_form.html'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user = self.request.user

        if not user.is_authenticated:
            return redirect('users:login')

        if not user.has_perm('catalog.moderating_products'):
            return redirect('users:error_permission')

        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        return reverse_lazy('users:user_products')


class CategoryUserListView(ListView):
    model = Category
    template_name = 'users/categories_for_content_manager.html'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user = self.request.user

        if not user.is_authenticated:
            return redirect('users:login')

        if not user.has_perm('catalog.management_category'):
            return redirect('users:error_permission')

        return self.render_to_response(self.get_context_data())


class ErrorPermissionTemplateView(TemplateView):
    template_name = 'users/permission_error.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_page'] = self.request.META.get('HTTP-REFERER')

        return context


class ChangePostBannedFormView(UpdateView):
    model = Post
    form_class = PostBannedForm
    template_name = 'users/post_banned_form.html'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user = self.request.user

        if not user.is_authenticated:
            return redirect('users:login')

        if not user.has_perm('catalog.management_posts'):
            return redirect('users:error_permission')

        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        return reverse_lazy('users:user_posts')





