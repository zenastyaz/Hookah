from django.urls import path

from core.views import index, about, contact, delivery, terms

urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('delivery', delivery, name='delivery'),
    path('terms', terms, name='terms'),
]
