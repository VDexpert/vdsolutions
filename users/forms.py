from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from catalog.forms_mixin import StyleFormMixin
from users.models import User
from users.utils import send_email_for_verify
from django.core.exceptions import ObjectDoesNotExist


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            User.objects.all().get(email=email)

        except ObjectDoesNotExist:
            self.add_error('username','У Вас нет аккаунта на портале. Перейдите по ссылке "Регистрация" внизу формы')

        else:

            if email is not None and password:
                self.user_cache = authenticate(self.request, email=email, password=password,)

                if self.user_cache is None:
                    self.add_error('username', '''Пароль введен неправильно''')
                    return False

                if not self.user_cache.email_verify:
                    send_email_for_verify(self.request, self.user_cache)
                    self.add_error('username', '''Ваша регистрация не была завершена, проверьте почту - 
                    мы отправили письмо с завершением регистрации. Оно могло попасть в папку "Спам"''')
                    #raise ValidationError('Ваша регистрация не была завершена, проверьте почту')  TODO: разобраться, почему эта команда не работает

                else:
                    self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class CustomPasswordResetForm(StyleFormMixin, forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            user = User.objects.all().get(email=email)

        except User.DoesNotExist:
            self.add_error('email', 'У Вас нет аккаунта на портале. Перейдите по ссылке "Регистрация" внизу формы')

        else:

            if not user.email_verify:
                self.add_error('email', '''Ваша регистрация не была завершена, проверьте почту - 
                    мы отправили письмо с завершением регистрации. Оно могло попасть в папку "Спам"''')
                return False

            return email


class CustomUserEditForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'country', 'phone')