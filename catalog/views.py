from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from catalog.forms import PostForm, CategoryFormUpdate, CategoryFormCreate, FeedbackForm, ChangeBlogForm
from catalog.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView, FormView
from catalog.auxfunc import translit
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.cache import cache


class ProductHomeListView(ListView):
    model = Product
    paginate_by = 12
    template_name = 'catalog/home.html'
    paginate_orphans = 3

    def get_queryset(self):
        return super().get_queryset().filter(status=Product.STATUS_ACTIVE, banned='одобрено модератором').order_by('-absolute_top')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [x for x in Category.objects.all() if Product.objects.all().filter(category=x)]
        context['versions'] = Version.objects.all()
        context['count_products'] = self.get_queryset().count()
        context['home'] = Home.objects.all().first()

        return context


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'catalog/form_category.html'
    form_class = CategoryFormCreate
    success_url = reverse_lazy('users:categories_for_content_manager')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user = self.request.user

        if not user.is_authenticated:
            return redirect('users:login')

        if user.has_perm('catalog.management_category'):
            return self.render_to_response(self.get_context_data())
        else:
            return redirect('users:error_permission')

    def form_valid(self, form):
        self.object = form.save()
        self.object.slug = translit.do(self.object.category_name)
        self.object.save()

        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'catalog/form_category.html'
    form_class = CategoryFormUpdate
    success_url = reverse_lazy('users:categories_for_content_manager')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user = self.request.user

        if not user.is_authenticated:
            return redirect('users:login')

        if user.has_perm('catalog.management_category'):
            return self.render_to_response(self.get_context_data())

        else:
            return redirect('users:error_permission')

    def form_valid(self, form):
        self.object = form.save()
        self.object.slug = translit.do(self.object.category_name)
        self.object.save()

        return super().form_valid(form)


class CategoryWithProductsDetailView(DetailView):
    model = Category
    template_name = 'catalog/category_with_products.html'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        if not Product.objects.all().filter(category=self.object.pk).exists():
            return redirect('catalog:double_404_page')

        return self.render_to_response(self.get_context_data())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        products_category = Product.objects.all().filter(status=Product.STATUS_ACTIVE, banned='одобрено модератором', category=self.object.pk).order_by('-absolute_top')
        paginator = Paginator(products_category, 12)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['categories'] = [x for x in Category.objects.all() if Product.objects.all().filter(category=x)]
        context['page_obj'] = page_obj
        context['versions'] = Version.objects.all()
        context['count_products'] = products_category.count()
        context['paginator'] = paginator
        context['products'] = paginator.page(int(str(page_obj).split(' ')[1])).object_list

        return context


class ProductDetailView(DetailView):
    model = Product
    slug_url_kwarg = 'prod_slug'
    form = FeedbackForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['versions'] = Version.objects.all().filter(product=self.object.pk)
        context['form'] = self.form
        #context['object'] = self._cache_product()

        return context

    def post(self, form, *args, **kwargs):
        send_mail(
            subject='''Вопрос по Вашему продукту от посетителя Skystore''',
            message=f'''Продукт '{self.request.POST['product']}'
            \nИмя посетителя: {self.request.POST['name']}
            \nEmail посетителя: {self.request.POST['email']}
            \nСообщение посетителя: \n{self.request.POST['message']}''',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.request.POST['product_owner']]
        )

        return redirect('catalog:after_ordering')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/delete_product.html'
    success_url = reverse_lazy('users:user_products')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user = self.request.user

        if not user.is_authenticated:
            return redirect('users:login')

        if user.has_perm('catalog.moderating_products') or user.has_perm('catalog.management_category') \
                or user.has_perm('catalog.management_posts'):
            return redirect('users:error_permission')

        if not user.has_perm('catalog.delete_product'):
            return redirect('users:error_permission')

        return self.render_to_response(self.get_context_data())

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)

        return queryset


class PostListView(ListView):
    model = Post
    paginate_by = 12
    template_name = 'catalog/post_list.html'
    ordering = ['-create_at']
    paginate_orphans = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [x for x in Category.objects.all() if Post.objects.all().filter(category=x)]
        context['count_posts'] = self.get_queryset().count()
        context['blog'] = Blog.objects.all().first()

        return context

    def get_queryset(self):
        return super().get_queryset().filter(status=Post.STATUS_ACTIVE, banned=Post.BANNED_FALSE).order_by('-create_at')


class CategoryWithPostsDetailView(DetailView):
    model = Category
    template_name = 'catalog/category_with_posts.html'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        if not Post.objects.all().filter(category=self.object.pk).exists():
            return redirect('catalog:double_404_page')

        return self.render_to_response(self.get_context_data())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        posts_category = Post.objects.all().filter(status=Post.STATUS_ACTIVE, category=self.object.pk, banned=Post.BANNED_FALSE).order_by('-create_at')
        paginator = Paginator(posts_category, 12)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['categories'] = [x for x in Category.objects.all() if Post.objects.all().filter(category=x)]
        context['page_obj'] = page_obj
        context['versions'] = Version.objects.all()
        context['count_posts'] = posts_category.count()
        context['paginator'] = paginator
        context['posts'] = paginator.page(int(str(page_obj).split(' ')[1])).object_list

        return context


class PostDetailView(DetailView):
    model = Post
    slug_url_kwarg = 'post_slug'
    form = FeedbackForm()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object = self.get_object()
        context = super().get_context_data(object=self.object)
        context['form'] = self.form

        self.object.count_views += 1
        self.object.save()

        if self.object.count_views == 100:
            send_mail(
                subject='100 просмотров на публикации',
                message=f'Публикация "{self.object.title}" набрала 100 просмотров!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.request.user.email,]
            )

        return super().render_to_response(context)

    def post(self, request, *args, **kwargs):
        send_mail(
            subject='''Вопрос по Вашей статье от посетителя Skystore''',
            message=f'''Статья: '{self.request.POST['post']}'
                        \nИмя посетителя: {self.request.POST['name']}
                        \nEmail посетителя: {self.request.POST['email']}
                        \nСообщение посетителя: \n{self.request.POST['message']}''',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.request.POST['post_owner']]
        )

        return redirect('catalog:after_ordering')


class PostCreateView(CreateView):
    model = Post
    template_name = 'catalog/form_post.html'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user = self.request.user

        if not user.is_authenticated:
            return redirect('users:login')

        if user.has_perm('catalog.moderating_products') or user.has_perm('catalog.management_category') \
                or user.has_perm('catalog.management_posts'):
            return redirect('users:error_permission')

        if not user.has_perm('catalog.add_post'):
            return redirect('users:error_permission')

        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.slug = translit.do(self.object.title)
        self.object.change_at = timezone.now()
        self.object.save()

        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'catalog/form_post.html'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user = self.request.user

        if not user.is_authenticated:
            return redirect('users:login')

        if user.has_perm('catalog.management_posts'):
            return self.render_to_response(self.get_context_data())

        if user.has_perm('catalog.moderating_products'):
            return redirect('users:error_permission')

        if not user.has_perm('catalog.change_post'):
            return redirect('users:error_permission')

        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        self.object = form.save()
        self.object.slug = translit.do(self.object.title)
        self.object.change_at = timezone.now()
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:user_posts')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'catalog/delete_post.html'
    success_url = reverse_lazy('users:user_posts')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user = self.request.user

        if not user.is_authenticated:
            return redirect('users:login')

        if not user.has_perm('catalog.delete_post'):
            return redirect('users:error_permission')

        if user.has_perm('catalog.moderating_products') or user.has_perm('catalog.management_category') \
                or user.has_perm('catalog.management_posts'):

            return redirect('users:error_permission')

        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        return reverse_lazy('users:user_posts')

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)

        return queryset


class ContactsFormView(FormView):
    template_name = 'catalog/contacts.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('catalog:after_feedback')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contacts.objects.all().get(id=1)

        return context

    def form_valid(self, form):
        send_mail(
            subject='''Обратная связь от посетителя Skystore в форме Контакты''',
            message=f'''Имя посетителя: {form.data['name']}
            \nEmail посетителя: {form.data['email']}
            \nСообщение посетителя: {form.data['message']}''',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[x.email for x in User.objects.all().filter(groups__name='Менеджеры')]
        )

        return super().form_valid(form)


class ChangeBlogUpdateView(UpdateView):
    model = Blog
    template_name = 'catalog/form_blog.html'
    form_class = ChangeBlogForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user = self.request.user

        if not user.is_authenticated:
            return redirect('users:login')

        if not user.has_perm('catalog.management_posts') or not user.has_perm('catalog.management_category'):
            return redirect('users:error_permission')

        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        return Blog.objects.first()

    def get_success_url(self):
        return reverse_lazy('users:user_posts')


def page_not_found_view(request, exception):
    return render(request, 'page_404.html', status=404)
