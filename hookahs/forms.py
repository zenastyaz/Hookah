import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Flavor, OrderKeitering


class HookahFilterForm(forms.Form):
    name = forms.CharField(required=False, label='Name')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category')
    flavors = forms.ModelMultipleChoiceField(queryset=Flavor.objects.all(), required=False, label='Flavors')


class OrderKeiteringForm(forms.ModelForm):
    class Meta:
        model = OrderKeitering
        fields = ['standard_qty', 'premium_qty', 'hours', 'delivery', 'phone', 'name', 'address']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+?\d{10,15}$', phone):
            raise ValidationError(
                'Введите корректный номер телефона. Он может начинаться с "+", а также должен содержать от 10 до 15 цифр.')
        return phone

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'^[A-Za-zА-Яа-яЁё\s]+$', name):
            raise ValidationError('Имя должно содержать только буквы и пробелы.')
        return name

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if len(address) < 10:
            raise ValidationError('Адрес слишком короткий, введите полный адрес.')
        return address
