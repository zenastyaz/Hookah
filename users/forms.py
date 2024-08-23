from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, UsernameField
from .models import User, Address


class EmailVerificationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Электронная почта"}))
    verification_code = forms.CharField(max_length=4, widget=forms.TextInput(attrs={"placeholder": "Код верификации"}))

    class Meta:
        model = User
        fields = [
            'email',
            'verification_code',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserRegisterForm(UserCreationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Подтвердите пароль"}))

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


class UpdateProfileForm(UserChangeForm):
    username = UsernameField(disabled=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "email"}))

    class Meta:
        model = User
        fields = [
            'email',
            'username',
        ]


class AddressForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Имя"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Фамилия"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "+357********"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Адрес"}))

    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone', 'address']


AddressFormSet = inlineformset_factory(User, Address, form=AddressForm, extra=0, can_delete=True)


class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
