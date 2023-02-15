from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView
from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version, Category
from catalog.auxfunc import translit
from django.utils import timezone


class ProductCreateWithVersionView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/form_product_with_versions.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_authenticated:
            return redirect('users:login')

        if user.has_perm('catalog.moderating_products') or user.has_perm('catalog.management_posts') \
                or user.has_perm('catalog.management_category'):
            return redirect('users:error_permission')

        if not user.has_perm('catalog.add_product'):
            return redirect('users:error_permission')

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('users:user_products')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        FormSet = inlineformset_factory(self.model, Version, form=VersionForm, extra=5)

        if self.request.method == 'POST':
            formset = FormSet(self.request.POST, instance=self.object)

        else:
            formset = FormSet(instance=self.object)

        context_data['formset'] = formset

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        active_versions = len([x for x in form.data.values() if x == 'активно'])

        if active_versions > 1:
            form.error_status = 'Необходимо, чтобы только одна версия вашей программы была активной'

            return self.render_to_response(self.get_context_data(form=form))

        with transaction.atomic():
            if form.is_valid():
                if formset.is_valid():
                    formset.instance = form.save()
                    formset.save()
                else:
                    return self.render_to_response(self.get_context_data(form=form))

            self.object = form.save()
            self.object.user = self.request.user
            self.object.slug = translit.do(self.object.product_name)
            self.object.change_range_prod_at = timezone.now()
            self.object.save()
            id_category = form.data['category']
            category = Category.objects.all().get(id=id_category)
            category.add_new_prod = timezone.now()
            category.save()

            return super().form_valid(form)


class ProductWithVersionUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/form_product_with_versions.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_authenticated:
            return redirect('users:login')

        if user.has_perm('catalog.management_posts') or user.has_perm('catalog.management_category'):
            return redirect('users:error_permission')

        if not user.has_perm('catalog.change_product'):
            return redirect('users:error_permission')

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.has_perm('catalog.moderating_products'):
            return super().get_queryset()

        return super().get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('users:user_products')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        count_versions = Version.objects.all().filter(product=self.object.pk).count()
        FormSet = inlineformset_factory(self.model, Version, form=VersionForm, extra=1000, max_num=count_versions + 1)

        if self.request.method == 'POST':
            formset = FormSet(self.request.POST, instance=self.object)
        else:
            formset = FormSet(instance=self.object)
        context_data['formset'] = formset

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        active_versions = len([x for x in form.data.values() if x == 'активно'])

        if active_versions > 1:
            form.error_status = 'Необходимо, чтобы только одна версия вашей программы была активной'

            return self.render_to_response(self.get_context_data(form=form))

        if form.is_valid():
            self.object = form.save()
            self.object.slug = translit.do(self.object.product_name)
            self.object.save()

            if formset.is_valid():
                formset.instance = form.save()
                formset.save()
            else:
                return self.render_to_response(self.get_context_data(form=form))

        return super().form_valid(form)
