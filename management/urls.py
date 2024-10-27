from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='admin-home'),

    #product
    path('product/', product_list, name='product'),
    path('product/edit/', edit_product, name='edit_product'),
    path('product/details/<int:id>/', product_details, name='product_details'),
    path('add-product/', add_product, name='add_product'),
    path('edit-product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('manage-order/', order_manage, name='order_manage'),
    path('order/<int:order_id>/', order_details_view, name='order_details'),
    path('update-shipping/', update_shipping_view, name='update_shipping'),


    #htmx
    path('mark-order-as-done/<int:order_id>/', mark_order_as_done, name='mark_order_as_done'),

    path('change-password/', change_password, name='change_password'),

    #admin_login
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='admin_logout'),

    path('upload/', upload_image, name='upload_image'),
    path('revert/', revert_image, name='revert_image'),
]