import json
import stripe
from datetime import datetime

from django.views.generic import ListView, DetailView, View
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django_filters.views import FilterView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from hookahs.models import Hookah, Cart, Category, Flavor, Order
from users.models import User, Address
from hookahs.forms import OrderKeiteringForm
from hookahs.filters import ProductFilter
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


def services(request):
    return render(request, 'services.html')


class HookahListView(FilterView):
    template_name = 'hookah_list.html'
    model = Hookah
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('is_available')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['flavor_list'] = Flavor.objects.all()
        context['selected_flavors'] = self.request.GET.getlist('flavors')
        return context


@login_required
@require_POST
def add_like(request, pk):
    user = request.user
    hookah = get_object_or_404(Hookah, pk=pk)
    is_favorite = user in hookah.my_favorites.all()

    if is_favorite:
        hookah.my_favorites.remove(user)
        liked = False
    else:
        hookah.my_favorites.add(user, through_defaults={})
        liked = True

    hookah.save()

    return JsonResponse({'liked': liked, 'likes_count': hookah.my_favorites.count()})


class MyFavourite(LoginRequiredMixin, FilterView):
    template_name = 'hookah_list.html'
    model = Hookah
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = self.request.user.liked_by.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['flavor_list'] = Flavor.objects.all()
        context['selected_flavors'] = self.request.GET.getlist('flavors')
        return context


class MyCart(LoginRequiredMixin, ListView):
    template_name = 'cart.html'
    model = Hookah

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()
        total_cost = sum(item.total_price for item in cart_items)
        context['total_cost'] = total_cost

        has_hookah = any(item.hookah.category and item.hookah.category.name == 'Кальян' for item in cart_items)
        has_tobacco = any(item.hookah.category and item.hookah.category.name == 'Табак' for item in cart_items)

        context['has_hookah'] = has_hookah
        context['has_tobacco'] = has_tobacco

        return context


class ProceedWithoutItemsView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        no_need_hookah = request.POST.get('no_need_hookah')
        no_need_tobacco = request.POST.get('no_need_tobacco')

        if no_need_hookah or no_need_tobacco:
            return redirect('checkout')

        return redirect('hookah-cart')


@login_required
def add_cart(request, pk):
    if request.method == "POST":
        user = request.user
        hookah = get_object_or_404(Hookah, id=pk)
        booking_date = request.POST['booking_date']
        booking_time = request.POST['booking_time']

        booking_datetime_str = f"{booking_date} {booking_time}"
        booking_time_obj = datetime.strptime(booking_time, '%H:%M').time()
        if booking_time_obj not in hookah.get_available_times(datetime.strptime(booking_date, '%Y-%m-%d').date()):
            return redirect('hookah', pk=pk)

        cart_item, created = Cart.objects.get_or_create(
            user=user,
            hookah=hookah,
            booking_date=booking_date,
            booking_time=booking_time_obj,
        )
        if not created:
            cart_item.quantity += 1
        cart_item.save()

        return redirect('hookah-cart')
    return redirect('hookah', pk=pk)


class CartChangeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
        action = request.POST.get('action')

        if action == 'add':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'subtract':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            elif cart_item.quantity == 1:
                cart_item.delete()
                total_cost = sum(item.total_price for item in Cart.objects.filter(user=request.user))
                return JsonResponse({'quantity': 0, 'total_cost': float(total_cost)}, status=200)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

        total_cost = sum(item.total_price for item in Cart.objects.filter(user=request.user))
        return JsonResponse({'quantity': cart_item.quantity, 'total_cost': float(total_cost)}, status=200)


class CartRemoveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
        cart_item.delete()
        return redirect('hookah-cart')


class HookahlDet(DetailView):
    template_name = 'hookah.html'
    model = Hookah

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hookah = self.get_object()
        available_times = []

        if 'booking_date' in self.request.GET:
            booking_date = self.request.GET['booking_date']
            try:
                date_obj = datetime.strptime(booking_date, '%Y-%m-%d').date()
                available_times = hookah.get_available_times(date_obj)
            except ValueError:
                available_times = []

        context['available_times'] = available_times
        return context


def create_order(request):
    if request.method == 'POST':
        form = OrderKeiteringForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'order_form.html', {'form': form, 'success': True})
    else:
        form = OrderKeiteringForm()

    return render(request, 'order_form.html', {'form': form})


class PaymentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Некорректный JSON")

        address_id = data.get('address_id')
        people = data.get('people')
        hookah_master = data.get('hookahMaster', False)
        delivery_option = data.get('delivery_option')
        payment_method_id = data.get('payment_method_id')

        if not address_id or not people:
            return JsonResponse({'error': 'Пожалуйста, выберите адрес и заполните все поля.'}, status=400)

        try:
            delivery_address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return JsonResponse({'error': 'Адрес не найден.'}, status=400)

        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.total_price for item in cart_items)
        delivery_cost = 10 if delivery_option == 'delivery' else 0
        hookah_master_cost = 10 if hookah_master else 0
        total_price_with_additions = total_price + delivery_cost + hookah_master_cost

        try:
            intent = stripe.PaymentIntent.create(
                amount=int(total_price_with_additions * 100),
                currency='eur',
                payment_method_types=['card'],
            )
        except stripe.error.StripeError as e:
            return JsonResponse({'error': f'Ошибка Stripe: {str(e)}'}, status=400)

        try:
            confirmed_intent = stripe.PaymentIntent.confirm(
                intent['id'],
                payment_method=payment_method_id,
            )
        except stripe.error.StripeError as e:
            return JsonResponse({'error': f'Ошибка Stripe при подтверждении: {str(e)}'}, status=400)

        if confirmed_intent['status'] == 'succeeded':
            for item in cart_items:
                Order.objects.create(
                    user=request.user,
                    hookah=item.hookah,
                    quantity=item.quantity,
                    booking_date=item.booking_date,
                    booking_time=item.booking_time,
                    delivery_address=delivery_address,
                    number_of_people=int(people),
                    hookah_master=hookah_master
                )
            cart_items.delete()
            return JsonResponse({'success': 'Платеж прошел успешно и заказ создан.'})
        else:
            return JsonResponse({'error': f'Платеж не был завершен. Статус: {confirmed_intent["status"]}'}, status=400)

    def get(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        addresses = Address.objects.filter(user=request.user)
        total_price = sum(item.total_price for item in cart_items)
        return render(request, 'checkout.html', {
            'object_list': cart_items,
            'addresses': addresses,
            'total_price': total_price,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        })


class Checkout(LoginRequiredMixin, ListView):
    template_name = 'checkout.html'
    model = Cart

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_price = sum(item.total_price for item in context['object_list'])
        context['total_price'] = total_price
        context['addresses'] = Address.objects.filter(user=self.request.user)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


# class CheckoutView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         cart_items = Cart.objects.filter(user=request.user)
#
#         has_hookah = any(item.hookah.category and item.hookah.category.name == 'Кальян' for item in cart_items)
#         has_tobacco = any(item.hookah.category and item.hookah.category.name == 'Табак' for item in cart_items)
#
#         return render(request, 'cart.html', {
#             'cart_items': cart_items,
#             'total_cost': sum(item.total_price for item in cart_items),
#             'has_hookah': has_hookah,
#             'has_tobacco': has_tobacco
#         })

