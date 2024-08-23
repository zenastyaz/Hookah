from django.urls import path
from users.views import (
    RegisterView,
    LoginView,
    LogoutView,
    EmailVerificationView,
    ProfileView,
    AddAddressView,
    ViewAddresses,
    DeleteAddressView)
from users.utils import send_verification_code_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('add_address/', AddAddressView.as_view(), name='add_address'),
    path('addresses_list/', ViewAddresses.as_view(), name='addresses_list'),
    path('delete_address/<int:pk>/', DeleteAddressView.as_view(), name='delete_address'),
    path('send-verification-code/', send_verification_code_view, name='send_verification_code'),
    path('verification/', EmailVerificationView.as_view(), name='verification'),
]
