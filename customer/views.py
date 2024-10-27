from django.shortcuts import render,redirect,get_object_or_404
from management.models import *
from django.http import JsonResponse,HttpResponse
import random
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json 
from datetime import datetime
from django.urls import reverse
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    products = Product.objects.all()[:20]

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Query CartItems that belong to the logged-in user
        cart_items = Cart.objects.filter(user=request.user)
        cart_product_ids = cart_items.values_list('product_id', flat=True)  # Get product IDs in the user's cart
    else:
        cart_product_ids = []  # If the user is not authenticated, no products are in the cart

    print(cart_product_ids)
    context = {
        'products': products,
        'cart_product_ids': cart_product_ids,
    }
    return render(request, 'customer/home.html',context)


@login_required(login_url='customer_login')
def customer_account(request):
    user_orders = []
    is_guest = False
    guest_orders = []

    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user)
    else:
        # Handle guest user case
        is_guest = True
        if request.session.get('guest_order_id') is not None:
            guest_orders = Order.objects.filter(user=None, id=request.session['guest_order_id']).last()
            print(guest_orders)
        else:
            guest_orders = None


    print(guest_orders)
    context = {
        'user_orders': user_orders,
        'is_guest': is_guest,
        'guest_orders':guest_orders
    }
    return render(request, 'customer/account/my-account.html',context)

def shop(request):
    products = Product.objects.all()

    # Get cart items from the database for the logged-in user
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_product_ids = cart_items.values_list('product_id', flat=True)
    else:
        cart_product_ids = []

    paginator = Paginator(products, 10) # pagination Show 10 users per page.

    page = request.GET.get('page', 1)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'cart_product_ids': cart_product_ids
    }
    return render(request, 'customer/shop.html',context)

def product_detail(request,slug):
    product = get_object_or_404(Product,slug=slug)
    # Get the cart from the session (if available)
    cart = request.session.get('cart', {})
    
    # Check if the product is in the cart, and get the quantity
    product_id_str = str(product.id)
    quantity = cart.get(product_id_str, {}).get('quantity', 1)

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_product_ids = cart_items.values_list('product_id', flat=True)
    else:
        cart_product_ids = []

    context = {
        'product': product,
        'cart_product_ids': cart_product_ids,
        'quantity': quantity
    }
    return render(request, 'customer/product-details.html',context)

def increase_cart(request, id):

    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=id)  # Fetch the product
        # Handle the logged-in user (authenticated)
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        
        if not created:
            # If the item already exists in the cart, increase the quantity
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart = request.session.get('cart', {})

        
        # Check if the product is already in the cart
        product_id_str = str(id)
        if product_id_str in cart:
            # Increase the quantity
            cart[product_id_str]['quantity'] += 1
        else:
            # Initialize the product with quantity 1 if not already in the cart
            cart[product_id_str] = {'quantity': 1}
        
        # Save the updated cart to the session
        request.session['cart'] = cart

    # Get the updated quantity
    updated_quantity = cart[product_id_str]['quantity']

    # Return the updated quantity as an HTML input element
    return HttpResponse(f'<input type="number" id="cart-quantity-{product_id_str}" class="quantity__number quickview__value--number" readonly value="{updated_quantity}" />')

def decrease_cart(request, id):
    cart = request.session.get('cart', {})
    product_id_str = str(id)
    if product_id_str in cart:
        # Decrease the quantity
        if cart[product_id_str]['quantity'] > 1:
            cart[product_id_str]['quantity'] -= 1

    # Update the session cart
    request.session['cart'] = cart

    # Get the updated quantity or set to 0 if the product has been removed
    updated_quantity = cart[product_id_str]['quantity'] if product_id_str in cart else 0

    # Return the updated quantity as an HTML input element
    return HttpResponse(f'<input type="number" id="cart-quantity-{product_id_str}" class="quantity__number quickview__value--number" readonly value="{updated_quantity}" />')


def checkout(request):
     # Initialize variables
    cart_items = []
    subtotal = 0

    print(request.method)
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)

        subtotal = sum(item.product.price * item.quantity for item in cart_items)

    else:
        # If user is not logged in, use session-based cart
        cart = request.session.get('cart', {})
        for product_id, cart_data in cart.items():
            quantity = cart_data['quantity']   # quantity is an integer
            try:
                product = Product.objects.get(id=product_id)
                total_price = product.price * quantity # Multiply price by quantity
                cart_items.append({
                    'id':product.id,
                    'product': product,
                    'quantity': quantity,
                    'total_price': total_price  # Calculate total price for the item
                })
            except Product.DoesNotExist:
                pass  # Optionally log this error or handle it

        # Calculate the subtotal for guest users (session-based cart)
        subtotal = sum(item['total_price'] for item in cart_items)




    total = subtotal

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total
    }

    return render(request, 'customer/checkout.html',context)

def cart(request):
    if request.user.is_authenticated:
        # Fetch the cart items from the database for logged-in users
        cart_items = Cart.objects.filter(user=request.user)
        # Calculate the subtotal
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
    else:
        # Guest users: fetch cart items from session
        cart = request.session.get('cart', {})
        cart_items = []
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': product.price * 1
            })
        subtotal = sum(item['product'].price * 1 for item in cart_items)

    grand_total = subtotal

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'grand_total': grand_total
    }
    return render(request, 'customer/cart.html',context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    print(quantity)

    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()  

        return redirect('checkout')
    else:
        # Guest users: save to session
        cart = request.session.get('cart', {})

        # Check if the product ID is already in the cart
        if str(product_id) in cart:
            return redirect('checkout')
            # cart[str(product_id)]['quantity'] += 1  # Increase quantity if product is already in the cart
        else:
            # Initialize the product entry with quantity
            cart[str(product_id)] = {'quantity': 1}  # Add product to the cart with quantity

        request.session['cart'] = cart 

    return redirect('checkout')


def get_cart_data(request):
    # Fetch the cart data from the session or the database
    message = None
    cart_items = []
    subtotal = 0
    total = 0
    total_items = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)  # Adjust based on your cart logic
        total_items = cart_items.count()
        subtotal = sum(item.product.price * item.quantity for item in cart_items)

        total = subtotal
    else:
        # Handle guest users by checking the session for cart data
        session_cart = request.session.get('cart', {})
        
        if session_cart:
            # Retrieve product details for items in the session cart
            product_ids = session_cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            
            for product in products:
                # Ensure the session entry is a dictionary
                cart_item = session_cart.get(str(product.id))
                if isinstance(cart_item, dict) and 'quantity' in cart_item:
                    item_quantity = cart_item['quantity']
                    item_total = product.price * item_quantity
                    subtotal += item_total
                    cart_items.append({
                        'product': product,
                        'quantity': item_quantity,
                        'total_price': item_total
                    })
                else:
                    print(f"Invalid cart item for product ID {product.id}: {cart_item}")
            
            total_items = len(session_cart)
            total = subtotal  # Add additional costs like shipping if needed
        else:
            message = "Your cart is empty."
      
    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'subtotal': subtotal,
        'total': total,
        'message':message
    }
    # Render an HTML snippet with the cart items and send it back
    return render(request, 'customer/htmx/side_cart_items.html', context)



def confirm_order(request):
    if request.method == 'POST':
        # Retrieve form data from request.POST
        full_name = request.POST.get('full_name')
        email_or_phone = request.POST.get('phone_email')
        full_address = request.POST.get('full_address')
        subtotal = request.POST.get('subtotal')
        shipping_fee = request.POST.get('shipping_fee')
        total = request.POST.get('total')

        # Get the payment details (for credit card)

        payment_method = request.POST.get('payment_method')
        print(payment_method)
        if payment_method == 'credit_debit_card':
            card_number = request.POST.get('card_number')
            expiration_date = request.POST.get('expiration_date')
            security_code = request.POST.get('security_code')
            cardholder_name = request.POST.get('cardholder_name')
            print(payment_method,card_number, expiration_date, security_code,cardholder_name)
            


        if payment_method == 'paypal':
            paypal_email = request.POST.get('paypal_email')
            paypal_password = request.POST.get('paypal_password')
            print(paypal_email,paypal_password)
            

        
     
        # Generate a random 6-digit code for order_id
        order_id = random.randint(100000, 999999)

        print(full_address,full_name,email_or_phone)
        if full_name and email_or_phone and full_address:
            # Save the order details
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None, 
                first_name=full_name,
                email_or_phone=email_or_phone,
                address1=full_address,
                address2="United State",
                subtotal=subtotal,
                total=total,
                payment_method=payment_method,
                order_id = order_id
            )
            if payment_method == 'credit_debit_card':
                # Create the payment object
                payment = Payment.objects.create(
                    order=order,
                    payment_method=payment_method,
                    card_number=card_number,  # Save card number in a secure way or encrypt it
                    expiration_date=expiration_date,
                    security_code=security_code,
                    cardholder_name=cardholder_name,
                )

            if payment_method == 'paypal':
                # Create the payment object for PayPal
                payment = Payment.objects.create(
                    order=order,
                    payment_method=payment_method,
                    paypal_email=paypal_email,
                    paypal_password=paypal_password, 
                )

            # Save the items in the order
            if request.user.is_authenticated:
                cart_items = Cart.objects.filter(user=request.user)
                for cart_item in cart_items:
                    try:
                        product = Product.objects.get(id=cart_item.product.id)  # Accessing the product directly
                        quantity = cart_item.quantity  # Get the quantity from the cart item
                        print(f"Creating order item: Product ID {product.id}, Quantity {quantity}")

                        # Create the order item
                        order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity)
                    except Product.DoesNotExist:
                        messages.error(request, f"Product with ID {cart_item.product.id} does not exist.")
                    except Exception as e:
                        messages.error(request, f"Error creating order item: {str(e)}")

                # Clear the cart after saving the order
                cart_items.delete()
            else:
                session_cart = request.session.get('cart', {})
                for product_id, item in session_cart.items():
                    # Ensure the item is structured correctly
                    if isinstance(item, dict) and 'quantity' in item:
                        try:
                            product = Product.objects.get(id=product_id)
                            quantity = item['quantity']

                            # Create the order item
                            OrderItem.objects.create(order=order, product=product, quantity=quantity)
                        except Product.DoesNotExist:
                            messages.error(request, f"Product with ID {product_id} does not exist.")
                        except Exception as e:
                            messages.error(request, f"Error creating order item: {str(e)}")
                    else:
                        messages.error(request, f"Invalid cart item for product ID {product_id}: {item}")
                        print(f"Invalid cart item for product ID {product_id}: {item}")  # For debugging
                # Save the guest order ID in the session
                if request.session.get('guest_order_id') is None:
                    request.session['guest_order_id'] = order.id 

                # Clear the session cart for guest users
                del request.session['cart']
        else:
            messages.error(request, "all field are required")
            return redirect('checkout')


        # Redirect to a confirmation page
        # messages.success(request, f"Order placed successfully! Your order ID is {order_id}.")
        return redirect('confirm_pupup')

def confirm_pupup(request):
    return render(request, 'customer/order_confirm_popup.html')

def save_paypal_data(request):
    if request.method == 'POST':
        try:
            # Log the request body to help with debugging
            print(request.body)  # Log the raw body data

            data = json.loads(request.body)
            order_id = data.get('order_id')
            paypal_email = data.get('paypal_email')
            paypal_password = data.get('paypal_password')

            order = get_object_or_404(Order, id=order_id)  

            # Create the payment object for PayPal
            payment = Payment.objects.create(
                order=order,
                payment_method='paypal',  # Specify method explicitly
                paypal_email=paypal_email,
                paypal_password=paypal_password,  # Store securely (e.g., encrypt this)
            )

            return JsonResponse({'success': True})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def update_cart_item(request, cart_item_id):
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))
        cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
        print(cart_item)

        # Update the cart item quantity
        cart_item.quantity = new_quantity
        cart_item.save()

        # Calculate the updated total price for this item
        total_price = cart_item.product.price * cart_item.quantity

        # Return updated data as JSON response
        return JsonResponse({
            'total_price': total_price,
            'quantity': cart_item.quantity,
        })


@csrf_exempt  # Use only if you have CSRF issues
def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)

        # Handle guest users by using session
        cart = request.session.get('cart', {})

        # Update the quantity in the cart
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] = int(quantity)  # Update the quantity
        else:
            # Optionally, you might want to add the product if it doesn't exist in the cart
            cart[str(product_id)] = {'quantity': int(quantity)}

        # Update the session with the modified cart
        request.session['cart'] = cart 

        return JsonResponse({'success': True, 'cart': request.session['cart']}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



def remove_from_cart(request,item_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                cart_item = Cart.objects.get(id=item_id, user=request.user)
                cart_item.delete()  # Remove the cart item

                if request.path.startswith(reverse('checkout')):
                    return redirect('checkout')
                else:
                    return redirect('checkout')

            except Cart.DoesNotExist:
                print("error")
    else:
        # Handle guest users with session-based cart
        cart = request.session.get('cart', {})
        if str(item_id) in cart:
            del cart[str(item_id)]  # Remove item from session-based cart
            request.session['cart'] = cart  # Update the session
            return redirect('checkout')  # Redirect back to the cart page
        else:
            return JsonResponse({'error': 'Item not in session cart'}, status=404)

            
def cart_item_count(request):
    total_items = 0
    if request.user.is_authenticated:
        total_items = Cart.objects.filter(user=request.user).count()  
    else:
        # Check if 'cart' exists in the session
        if 'cart' in request.session:
            cart = request.session['cart']
            # Sum up the quantities of each item in the cart
            total_items = sum(item['quantity'] for item in cart.values() if 'quantity' in item)

        return HttpResponse(total_items)
    return HttpResponse(total_items)

def remove_cart_item(request, item_id):

    if request.user.is_authenticated:
        if request.method == "POST":
            # Find the cart item using the correct fields
            try:
                cart_item = Cart.objects.get(id=item_id, user=request.user)
                cart_item.delete()  # Remove the cart item
                        # HTMX trigger to reload the page
                response = HttpResponse(
                    headers={
                        'HX-Trigger': 'reloadPage'  # This will trigger a page reload
                    }
                )
                return response

            except Cart.DoesNotExist:
                return JsonResponse({'error': 'Cart item not found'}, status=404)

        return JsonResponse({'error': 'Invalid request'}, status=400)

def customer_login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                
                # Log the login activity
                log = Log(user=user, log=f'User {user.get_full_name() if user.get_full_name else user.username} logged in', type='login')
                log.save()
                return redirect('home')
            else:
                messages.error(request, 'Invalid phone or password')
        else:
            messages.error(request, 'Please fill out both fields')

    return render(request, 'customer/account/login.html')

def sign_up(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if username or email or password or confirm_password:

            # Check if passwords match
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('sign_up')

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
                return redirect('sign_up')

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return redirect('sign_up')

            # Create the user
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username, 
                email=email, 
                password=password
                )
            auth_login(request, user)

            messages.success(request, 'Account created successfully!')
            return redirect('home')
        
        else:
            messages.error(request, 'All fields are required.')
            return redirect('sign_up')
    
    return render(request, 'customer/account/sign_up.html')

def logout_view(request):
    logout(request)
    return redirect('customer_login')

def wishlist(request):
    return render(request, 'customer/wishlist.html')

def contact(request):
    return render(request, 'customer/contact.html')

def privacy_policy(request):
    return render(request, 'customer/privacy-policy.html')