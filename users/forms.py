from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import User


class UserRegisterForm(UserCreationForm):

    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Введите пароль',
                                }))

    password2 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Повторите пароль',
                                }))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        widgets = {
            'email': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ваш email адрес',
            }),
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if len(password1) < 6:
            raise forms.ValidationError(
                "Пароль должен быть не менее 6 символов.")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password2 and password1 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        return password2


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(label='Email',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Ваш email адрес',
                               }))

    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Введите пароль',
                               }))


class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'Ваш email адрес',
                             }))

    first_name = forms.CharField(label='Имя',
                                 required=False,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                     'placeholder': 'Введите имя',
                                 }))

    last_name = forms.CharField(label='Фамилия',
                                required=False,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Введите фамилию',
                                }))

    avatar = forms.ImageField(label='Аватар',
                              required=False,
                              widget=forms.FileInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'Выберите аватар',
                              }))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar')
