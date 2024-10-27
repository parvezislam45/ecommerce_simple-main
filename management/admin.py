from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(ProductImage)
admin.site.register(DescriptionImage)
admin.site.register(Shipping)