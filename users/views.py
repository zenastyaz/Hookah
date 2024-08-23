import redis

from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from users.utils import send_welcome_email
from users.models import User, Address
from users.forms import (
    UserRegisterForm,
    UserLoginForm,
    UpdateProfileForm,
    EmailVerificationForm,
    AddressForm)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


class EmailVerificationView(FormView):
    template_name = 'verification.html'
    form_class = EmailVerificationForm
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        code = form.cleaned_data.get('verification_code')

        stored_code = redis_client.get(f'verification_code:{email}')
        if stored_code is None or stored_code.decode() != code:
            form.add_error('verification_code', 'Неправильный код верификации')
            return self.form_invalid(form)

        redis_client.delete(f'verification_code:{email}')
        return redirect(self.success_url)


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    model = User
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        send_welcome_email(form.instance)
        login(self.request, form.instance)
        return response


class LoginView(DjangoLoginView):
    template_name = 'login.html'
    form_class = UserLoginForm


class LogoutView(DjangoLogoutView):
    pass


class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'profile.html'
    form_class = UpdateProfileForm
    second_form_class = AddressForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs(), instance=self.request.user)

    def get_second_form(self):
        return self.second_form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address_form'] = self.get_second_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return redirect('profile')
        return self.form_invalid(form)


class AddAddressView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user = self.request.user
        address.save()
        return super().form_valid(form)


class ViewAddresses(LoginRequiredMixin, ListView):
    model = Address
    context_object_name = 'addresses'

    def get_queryset(self):
        return self.request.user.addresses.all()

    def render_to_response(self, context, **response_kwargs):
        addresses = list(self.get_queryset().values('first_name', 'last_name', 'phone', 'address', 'id'))
        return JsonResponse({'addresses': addresses})


class DeleteAddressView(LoginRequiredMixin, DeleteView):
    model = Address
    success_url = reverse_lazy('profile')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            self.object.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'У вас нет прав для удаления этого адреса.'})
