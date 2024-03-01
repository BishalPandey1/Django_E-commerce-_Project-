
from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('login/', signIn),
    path('register/', register),
    path('shop/', shop),
    path('cart/', cart),
    path('logout/', user_logout),
    path('product/<int:id>', productDetails),
    path('add-to-cart/<int:product_id>', addToCart),
    path('remove-from-cart/<int:cart_id>', removeFromCart),
    path('checkout/', checkout),
    path('orders/', orders),
    path('add-to-wishlist/<int:product_id>', add_to_wishlist),
    path('remove-from-wishlist/<int:wishlist_id>', remove_from_wishlist),
    path('wishlist/', wishlist),


#api urls
]
