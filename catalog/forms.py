from django import forms
from django.core.exceptions import ValidationError
from catalog.forms_mixin import StyleFormMixin
from catalog.models import Product, Version, Post, Category, Blog
from catalog.auxfunc import validator_version
import re


class CategoryFormCreate(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Category
        exclude = ('slug',)


class CategoryFormUpdate(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Category
        exclude = ('slug', 'category_name')


class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ('product_name', 'prod_annotation', 'description', 'picture', 'category', 'unit_price', 'status')

    def clean_product_name(self):
        name = self.cleaned_data['product_name']
        banned = ['казинo', 'криптовал', 'крипт', 'бирж', 'дешев', 'бесплатн', 'обман', 'полиц', 'радар']

        if len([x for x in banned if re.findall(x, name.lower())]):
            raise ValidationError(f'''Продукты типа '{name}' не разрешены на нашей площадке''')

        return name

    def clean_unit_price(self):
        price = self.cleaned_data['unit_price']

        if not price.isdigit():
            raise ValidationError(f'''В поле '{self.fields['unit_price'].label}' должны быть только цифры''')

        return price

    def clean_category(self):
        category = self.cleaned_data['category']

        if not category:
            raise ValidationError(f'''Поле '{self.fields['category'].label}' - обязательное, иначе Ваш продукт не будет показываться в каталоге''')

        return category

    def clean_description(self):
        description = self.cleaned_data['description']

        if not description:
            raise ValidationError(f'''Поле '{self.fields['description'].label}' - обязательное''')

        return description

    def clean_prod_annotation(self):
        prod_annotation = self.cleaned_data['prod_annotation']

        if not prod_annotation:
            raise ValidationError(f'''Поле '{self.fields['prod_annotation'].label}' - обязательное, иначе карточка не будет показываться в каталоге''')

        return prod_annotation


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

        if not category:
            raise ValidationError(f'''Поле '{self.fields['category'].label}' - обязательное, иначе Ваш продукт не будет показываться в каталоге''')

        return category

    def clean_content(self):
        content = self.cleaned_data['content']

        if not content:
            raise ValidationError(f'''Поле '{self.fields['content'].label}' - обязательное''')

        return content


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


class ChangeBlogForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Blog
        fields = '__all__'

    def clean_blog_h1(self):
        blog_h1 = self.cleaned_data['blog_h1']

        if not blog_h1:
            raise ValidationError(f'''Поле '{self.fields['blog_h1'].label}' - обязательное''')

        return blog_h1

    def clean_blog_annotation(self):
        blog_annotation = self.cleaned_data['blog_annotation']

        if not blog_annotation:
            raise ValidationError(f'''Поле '{self.fields['blog_annotation'].label}' - обязательное''')

        return blog_annotation

    def clean_title(self):
        title = self.cleaned_data['title']

        if not title:
            raise ValidationError(f'''Поле '{self.fields['title'].label}' - обязательное''')

        return title
