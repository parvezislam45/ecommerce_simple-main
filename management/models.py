from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100,blank=True, null=True)
    language = models.CharField(max_length=50,blank=True, null=True)
    profile_image = models.ImageField(upload_to='user/profile/images', blank=True, null=True)
    
    last_seen = models.DateTimeField(blank=True, null=True)

    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_email_active = models.BooleanField(default=False)
    forget_password_token = models.CharField(max_length=100,blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loguser")
    time = models.DateTimeField(auto_now_add=True)
    log = models.CharField(max_length=255, blank=True, null=True)  # Optional log field
    type = models.CharField(max_length=100,default='login')

    def __str__(self):
        return f"{self.user.username} logged in at {self.time} - {self.log if self.log else ''}"



class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='product_images/')
    stock = models.PositiveIntegerField()
    slug = models.SlugField(blank=True,null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='product_creator')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='product_updator')
    updated_on =  models.DateTimeField(auto_now=True)

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class DescriptionImage(models.Model):
    product = models.ForeignKey(Product, related_name='description_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_descriptions/')
    caption = models.CharField(max_length=255, blank=True, null=True)  # Optional image caption

    def __str__(self):
        return f"Image for {self.product.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,null=True, blank=True)
    email_or_phone = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255,null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50,null=True, blank=True)
    order_id = models.CharField(max_length=20, blank=True,null=True)
    status = models.BooleanField(default=False,blank=True,null=True)
    order_notes = models.CharField(max_length=300, blank=True,null=True)


    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_cr')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_up')
    updated_on =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.first_name}"
    class Meta:
        ordering = ['-id']

        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_debit_card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
    ]
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='order_payment')

    # Fields for Credit/Debit Cards
    card_number = models.CharField(max_length=16, blank=True, null=True)
    expiration_date = models.CharField(max_length=100,blank=True, null=True)
    security_code = models.CharField(max_length=4, blank=True, null=True)
    cardholder_name = models.CharField(max_length=100, blank=True, null=True)
    
    # Fields for PayPal
    paypal_email = models.EmailField(blank=True, null=True)
    paypal_password = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.get_payment_method_display()}"
    
class Shipping(models.Model):
    shipping_fee = models.IntegerField(default=100.00)