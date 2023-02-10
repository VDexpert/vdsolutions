from django import forms
from django.core.exceptions import ValidationError
from catalog.forms_mixin import StyleFormMixin
from catalog.models import Product, Version, Post, Category
from catalog.auxfunc import validator_version
import re


class CategoryFormCreate(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Category
        exclude = ('slug', 'none_products', 'none_posts')


class CategoryFormUpdate(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Category
        exclude = ('slug', 'category_name', 'none_products', 'none_posts')


class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ('product_name', 'description', 'picture', 'category', 'unit_price')

    def clean_product_name(self):
        name = self.cleaned_data['product_name']
        banned = ['казинo', 'криптовал', 'крипт', 'бирж', 'дешев', 'бесплатн', 'обман', 'полиц', 'радар']

        if len([x for x in banned if re.match(x, name.lower())]):
            print('исключение')
            raise ValidationError(f'''Продукты типа '{name}' не разрешены на нашей площадке''')

        return name

    def clean_unit_price(self):
        price = self.cleaned_data['unit_price']

        if not price.isdigit():
            raise ValidationError('В этом поле должны быть только цифры')

        return price


class VersionForm(StyleFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_status = None

    class Meta:
        model = Version
        fields = '__all__'

    def clean_value(self):
        value = self.cleaned_data['value']

        if not validator_version.do(value):
            raise ValidationError(f'Версия {value} не соотвествует формату: должны содержаться только цифры и точки')

        return value


class PostForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'picture', 'status', 'category')

    def clean_category(self):
        category = self.cleaned_data['category']
        print(category)

        if not category:
            raise ValidationError('Это поле обязательное - иначе Ваша публикация не будет показываться в блоге')

        return category

class ProductBannedForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ('banned',)


class FeedbackForm(StyleFormMixin, forms.Form):
    name = forms.CharField(max_length=50, label='Ваше имя', widget=forms.TextInput)
    email = forms.EmailField(max_length=50, label='Email для ответа', widget=forms.EmailInput)
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 3}), label="Ваше сообщение")


class PostBannedForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Post
        fields = ('banned',)
