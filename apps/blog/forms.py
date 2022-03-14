from re import M
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)

from auths.models import CustomUser


class CustomUserRegisterForm(UserCreationForm):  # noqa
    email = forms.EmailField(
        label='Email/имя пользователя',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    surname = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    date_birth = forms.DateField(
        label='Дата рожджения',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Select birthday',
                'type': 'date',
            },
            format=('%Y-%m-%d')
        )
    )

    class Meta:  # noqa
        model = CustomUser
        fields = ('email', 'password1', 'password2',
                  'name', 'surname', 'date_birth')
        # widgets = {
        #     'date_birth': forms.DateInput
        # }


class CustomerUserLoginForm(AuthenticationForm):  # noqa
    username = forms.EmailField(
        label='Email/username',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
