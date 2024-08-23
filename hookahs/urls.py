from django.urls import path

from hookahs.views import (
    services,
    HookahListView,
    add_like,
    MyFavourite,
    MyCart,
    add_cart,
    CartChangeView,
    CartRemoveView,
    HookahlDet,
    Checkout,
    ProceedWithoutItemsView,
    PaymentView,
    create_order,
)


urlpatterns = [
    path('', services, name='services'),
    path('list', HookahListView.as_view(), name='hookah-list'),
    path('hookah/<int:pk>/like/', add_like, name='hookah-like'),
    path('favorite', MyFavourite.as_view(), name='hookah-favorite'),
    path('cart', MyCart.as_view(), name='hookah-cart'),
    path('add-to-cart/<int:pk>/', add_cart, name='add-cart'),
    path('cart-change/<int:pk>/', CartChangeView.as_view(), name='change-cart'),
    path('cart-remove/<int:pk>/', CartRemoveView.as_view(), name='remove-cart'),
    path('proceed_without_items/', ProceedWithoutItemsView.as_view(), name='proceed_without_items'),
    path('<int:pk>/hookah/', HookahlDet.as_view(), name='hookah'),
    path('checkout', Checkout.as_view(), name='checkout'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('order/', create_order, name='create_order'),

]
