from .models import Items,CartItem

def all_items(request):
    links = Items.objects.all()
    return dict(links=links)

def cart_items(request):
    carts = CartItem.objects.all()
    total_quantity = sum(item.quantity for item in carts)
    total_price = sum(item.price * item.quantity for item in carts)
    cart_length = carts.count()
    return {
        'carts': carts,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'cart_length': cart_length,
    }

