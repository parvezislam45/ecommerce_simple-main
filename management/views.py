from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import *
from .decorators import superuser_required
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import get_valid_filename
from django.contrib.auth.hashers import make_password


# Create your views here.
@login_required(login_url='login')
@superuser_required
def home(request):
    return render(request, 'management/home.html')


@login_required(login_url='login')
@superuser_required
def add_product(request):
    if request.method == 'POST':
        # Get form data from request.POST and request.FILES
        product_name = request.POST.get('product_name')
        description = request.POST.get('description', '')
        product_code = request.POST.get('product_code', '')
        tags = request.POST.get('tags', '')
        regular_price = request.POST.get('regular_price', '0.00')
        sale_price = request.POST.get('sale_price', '0.00')
        image = request.FILES.get('main_image')

        print(product_name,description,sale_price,image)

        # Handle file uploads
        images = request.FILES.getlist('images')
        des_images = request.FILES.getlist('des_images')
        file = request.FILES.getlist('file')
        print("FILES data:", request.FILES)
        print("multi", images)

        print("ff",file)

        if product_name and description and sale_price and images:
            # Create a new Product object
            product = Product.objects.create(
                name=product_name,
                description=description,
                price=sale_price,
                image = images[0] if images else None,
                stock = 1,
                created_by = request.user
            )
            for img in des_images:
                DescriptionImage.objects.create(product=product,image=img)

            # Save the product images (if multiple, adjust as needed)
            print("61",images)
            for image in images:
                # Save each image in ProductImage model
                ProductImage.objects.create(product=product, image=image)
            return redirect('product')
    
    return render(request, 'management/add_product.html')


@csrf_exempt  # Temporarily disable CSRF if testing outside of a form
def upload_image(request):
    # Check if the request method is POST and file exists in request.FILES
    if request.method == 'POST' and 'file' in request.FILES:
        try:
            image = request.FILES['file']
            valid_filename = get_valid_filename(image.name)
            # Define where to temporarily save the uploaded image
            upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads', image.name)
            
            # Create the uploads directory if it doesn't exist
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            
            # Save the uploaded file to the specified path
            with open(upload_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            file_url = os.path.join(settings.MEDIA_URL, 'uploads', valid_filename)
            return JsonResponse({'file_path': file_url})
        
        except Exception as e:
            return JsonResponse({'error': f"File upload error: {str(e)}"}, status=500)
    
    # If request is not POST or no file was provided
    return JsonResponse({'error': 'Invalid request: Method not POST or no file provided'}, status=400)

@csrf_exempt
def revert_image(request):
    if request.method == 'DELETE':
        file_path = request.POST.get('file_path')
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            return JsonResponse({'success': True})
        return JsonResponse({'error': 'File not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def update_shipping_view(request):
    shipping_item = get_object_or_404(Shipping, id=1)
    if request.method == 'POST':
        shipping_fee = request.POST.get('shipping_fee')
        if shipping_fee:
            shipping_item.shipping_fee = shipping_fee
            shipping_item.save()
            return redirect('product')
    context = {
        'shipping_item': shipping_item
    }
    return render(request, 'management/update_shipping.html',context)

@login_required(login_url='login')
@superuser_required
def product_list(request):
    query = request.GET.get('q', '')

    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(name__icontains=query) |  # Search by product name
            Q(price__icontains=query)  # Search by price
        ).distinct()

    context = {
        "products":products
    }
    return render(request, 'management/product_list.html',context)


@login_required(login_url='login')
@superuser_required
def edit_product(request,product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Get form data from request.POST and request.FILES
        product.name = request.POST.get('product_name')
        product.description = request.POST.get('description', '')
        product.price = request.POST.get('sale_price', '0.00')
        # product.image = request.FILES.get('images')
        product.save()

        # Handle multiple image uploads
        images = request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        des_images = request.FILES.getlist('des_images')
        if des_images:
            for des_image in des_images:
                DescriptionImage.objects.create(product=product, image=des_image)
        return redirect('product')  

    return render(request, 'management/edit_product.html',{'product': product})

@login_required(login_url='login')
@superuser_required
def order_manage(request):
    query = request.GET.get('q', '') 
    orders = Order.objects.select_related('user').prefetch_related('items__product').all()
    if query:
        orders = orders.filter(
            Q(order_id__icontains=query) |  # Search by order_id
            Q(user__first_name__icontains=query) |  # Search by username (or name)
            Q(items__product__price__icontains=query)  # Search by product price
        ).distinct()

    context = {
        "orders": orders
        }
    return render(request, 'management/order_manage.html',context)

@login_required(login_url='login')
@superuser_required
def mark_order_as_done(request, order_id):

    message = None
    
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order.status = True
        order.save()
        message = "Order marked as done"
    
    return render(request, 'management/htmx/order_done_modal.html', {'order': order, 'message' : message})


@login_required(login_url='login')
@superuser_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('product') 



@login_required(login_url='login')
@superuser_required
def order_details_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Get the associated payment details
    payment = getattr(order, 'order_payment', None) 
    print(payment)
    context = {
        'order': order,
        'payment': payment
        # Add any other context needed for the template
    }
    return render(request, 'management/order_details.html', context)


@login_required(login_url='login')
@superuser_required
def product_details(request,id):
    product = get_object_or_404(Product, id=id)
    context = {
        "product": product
    }
    return render(request, 'management/product_details.html',context)


def change_password(request):
    message = None
    user = request.user
    print(user)
    
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        
        if new_password == confirm_password:
            user.password = make_password(new_password)
            user.save()
            print(new_password)
            message = 'Password changed successfully'
        else:
            message = 'Passwords do not match.'

    return render(request, "management/htmx/change_password_form.html", {"user": user, "message":message})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin-home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser:  # Check if the user is a superuser
                    auth_login(request, user)
                    # Redirect or return a response indicating successful login
                else:
               
                    messages.error(request, 'You do not have permission to log in.')
                
                # Log the login activity
                log = Log(user=user, log=f'User {user.get_full_name() if user.get_full_name else user.username} logged in', type='login')
                log.save()
                return redirect('admin-home')
            else:
                messages.error(request, 'Invalid phone or password')
        else:
            messages.error(request, 'Please fill out both fields')

    return render(request, 'account/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')