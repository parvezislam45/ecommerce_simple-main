# urls.py
from django.urls import path
from .views import ItemsListView, create_item_view,ItemDetailView,AddToCartView,remove_cart,OrderView,CartView,ItemUpdateView,create_item_view,items_list,ItemDeleteView

urlpatterns = [
    path('store/', ItemsListView.as_view(), name='store'),
    path('cart/', CartView.as_view(), name='cart'),
    path('create/', create_item_view, name='create'),
    path('store/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('all/', items_list, name='items-list'),
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='item-update'),
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='item-delete'),
    path('add_to_cart/<int:item_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete/<int:product_id>/',remove_cart,name='remove_cart'),
    path('order/', OrderView.as_view(), name='order'),
]
