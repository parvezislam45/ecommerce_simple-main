from rest_framework import generics
from .models import Items,CartItem
from .serializers import ItemsSerializer
from django.views.generic import ListView,DetailView
from django.views import View
from django.shortcuts import render, redirect,get_object_or_404
from .forms import ItemsForm
from django.http import JsonResponse
import json

class ItemsListView(ListView):
    model = Items
    template_name = 'store.html'
    context_object_name = 'items'
    

def create_item_view(request):
    if request.method == 'POST':
        form = ItemsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store')  # Adjust the redirect as needed
    else:
        form = ItemsForm()
    
    return render(request, 'post.html', {'form': form})
    
    
class ItemDetailView(DetailView):
    model = Items
    template_name = 'details.html' 
    context_object_name = 'item'
    
    
class AddToCartView(View):
    def post(self, request, item_id):
        item = get_object_or_404(Items, id=item_id)
        quantity = int(request.POST.get('quantity', 1))

     
        cart = request.session.get('cart', {})
        if str(item_id) in cart:
            cart[str(item_id)]['quantity'] += quantity
        else:
            cart[str(item_id)] = {
                'title': item.title, 
                'price': str(item.price), 
                'quantity': quantity, 
                'image': item.mainimage.url
            }
        request.session['cart'] = cart
        CartItem.objects.create(
            item=item,
            title=item.title,
            price=item.price,
            quantity=quantity,
            image=item.mainimage.url,
            user_id=None 
        )

        return redirect('order')
    
class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())
        return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})

    def post(self, request):
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            action = data.get('action')
            cart = request.session.get('cart', {})

            if item_id in cart:
                if action == 'increase':
                    cart[item_id]['quantity'] += 1
                elif action == 'decrease' and cart[item_id]['quantity'] > 1:
                    cart[item_id]['quantity'] -= 1
                elif action == 'delete':
                    del cart[item_id]  # Remove item from session cart
                    CartItem.objects.filter(item_id=item_id).delete()  # Remove item from database

                request.session['cart'] = cart
                total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())

                return JsonResponse({
                    'total_price': total_price,
                    'cart': cart
                })
            else:
                return JsonResponse({'error': 'Item not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


def remove_cart(request,product_id):
    product = Items.objects.get(id=product_id)
    session_id=request.session.session_key
    cart_id = CartItem.objects.get(cart_id = session_id)
    cart_item = CartItem.objects.get(product=product,cart=cart_id)
    cart_item.delete()
    return redirect('order')
    
class OrderView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        total_price = 0
        for item_id, item in cart.items():
            subtotal = float(item['price']) * item['quantity']
            item['subtotal'] = subtotal 
            total_price += subtotal 
        return render(request, 'order.html', {'cart': cart, 'total_price': total_price})

