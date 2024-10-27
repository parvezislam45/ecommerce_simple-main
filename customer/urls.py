from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('my-account/', customer_account, name='customer_account'),
  
    path('shop/', shop, name='shop'),
    path('checkout/', checkout, name='checkout'),
    path('product-detail/<slug:slug>/', product_detail, name='product_detail'),
    path('contact/', contact, name='contact'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('wishlist/', wishlist, name='wishlist'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('confirm_order/', confirm_order, name='confirm_order'),
    path('save_paypal_data/', save_paypal_data, name='save_paypal_data'),
    path('confirm_pupup/', confirm_pupup, name='confirm_pupup'),

    #htmx
    path('cart/data/', get_cart_data, name='get_cart_data'),
    path('cart-item-count/', cart_item_count, name='cart_item_count'),
    path('remove-cart-item/<int:item_id>/', remove_cart_item, name='remove_cart_item'),

    path('cart/update/<int:cart_item_id>/', update_cart_item, name='update_cart_item'),
    path('cart/update/<int:product_id>/', update_cart, name='update_cart'),
    path('increase-quantity/<int:id>/', increase_cart, name='increase'),
    path('decrease-quantity/<int:id>/', decrease_cart, name='decrease'),



    #authentication
    path('login/', customer_login_view, name='customer_login'),
    path('sign-up/', sign_up, name='sign_up'),
    path('logout/', logout_view, name='logout'),




]
