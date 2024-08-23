from django.db import models
from datetime import time


class Hookah(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, default=1)
    my_favorites = models.ManyToManyField('users.User', through='hookahs.Favorite', related_name='liked_by')
    my_cart = models.ManyToManyField('users.User', through='hookahs.Cart', related_name='my_cart')
    is_available = models.BooleanField(default=False)
    category = models.ForeignKey('hookahs.Category', on_delete=models.SET_NULL, null=True, blank=True)
    flavors = models.ForeignKey('hookahs.Flavor', on_delete=models.SET_NULL, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_available_times(self, date):
        weekday = date.weekday()

        if weekday in [0, 1, 2, 3]:
            start_hour = 13
            end_hour = 1
        elif weekday == 4:
            start_hour = 14
            end_hour = 2
        elif weekday == 5:
            start_hour = 14
            end_hour = 2
        else:
            start_hour = 13
            end_hour = 1

        if end_hour < start_hour:
            all_times = [time(hour, 0) for hour in range(start_hour, 24)] + [time(hour, 0) for hour in
                                                                             range(0, end_hour)]
        else:
            all_times = [time(hour, 0) for hour in range(start_hour, end_hour)]

        booked_times = Cart.objects.filter(hookah=self, booking_date=date).values_list('booking_time', flat=True)
        ordered_times = Order.objects.filter(hookah=self, booking_date=date).values_list('booking_time', flat=True)

        all_booked_times = set(booked_times) | set(ordered_times)
        available_times = [t for t in all_times if t not in all_booked_times]

        return available_times

    def __str__(self):
        return self.name


class Favorite(models.Model):
    hookah = models.ForeignKey('hookahs.Hookah', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    hookah = models.ForeignKey('hookahs.Hookah', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    booking_date = models.DateField(blank=True, null=True)
    booking_time = models.TimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    @property
    def total_price(self):
        return self.quantity * self.hookah.price


class Order(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True)
    hookah = models.ForeignKey('hookahs.Hookah', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    booking_date = models.DateField(blank=True, null=True)
    booking_time = models.TimeField(blank=True, null=True)
    hookah_master = models.BooleanField(default=False)
    number_of_people = models.IntegerField(default=1, null=True, blank=True)
    delivery_address = models.ForeignKey('users.Address', on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name


class Flavor(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class OrderKeitering(models.Model):
    standard_qty = models.PositiveIntegerField(verbose_name='Количество стандарт кальянов', default=0)
    premium_qty = models.PositiveIntegerField(verbose_name='Количество премиум кальянов', default=0)
    hours = models.PositiveIntegerField(verbose_name='Количество часов', default=1)
    delivery = models.BooleanField(verbose_name='Доставка', default=False)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    name = models.CharField(max_length=100, verbose_name='ФИО')
    address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итого')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def save(self, *args, **kwargs):
        standard_rate = 20
        premium_rate = 30

        standard_cost = self.standard_qty * self.hours * standard_rate
        premium_cost = self.premium_qty * self.hours * premium_rate

        delivery_cost = 10 if self.delivery else 0

        self.total_cost = standard_cost + premium_cost + delivery_cost

        super().save(*args, **kwargs)





