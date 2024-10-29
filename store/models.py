from django.db import models
from django.urls import reverse

class Items (models.Model):
     title = models.CharField(max_length=100,unique = True)
     slug = models.SlugField(max_length=100,unique = True)
     description = models.CharField(max_length=400,blank = True)
     price = models.DecimalField(max_digits=10, decimal_places=2)
     mainimage = models.ImageField(upload_to='photos/store',blank=True)
     subimage1 = models.ImageField(upload_to='photos/store',blank=True)
     subimage2 = models.ImageField(upload_to='photos/store',blank=True)
     subimage3 = models.ImageField(upload_to='photos/store',blank=True)
     subimage4 = models.ImageField(upload_to='photos/store',blank=True)
     subimage5 = models.ImageField(upload_to='photos/store',blank=True)
     subimage6 = models.ImageField(upload_to='photos/store',blank=True)
     subimage7 = models.ImageField(upload_to='photos/store',blank=True)
     subimage8 = models.ImageField(upload_to='photos/store',blank=True)
     desimage1 = models.ImageField(upload_to='photos/store',blank=True)
     desimage2 = models.ImageField(upload_to='photos/store',blank=True)
     desimage3 = models.ImageField(upload_to='photos/store',blank=True)
     desimage4 = models.ImageField(upload_to='photos/store',blank=True)
     desimage5 = models.ImageField(upload_to='photos/store',blank=True)
     desimage6 = models.ImageField(upload_to='photos/store',blank=True)
     desimage7 = models.ImageField(upload_to='photos/store',blank=True)
     desimage8 = models.ImageField(upload_to='photos/store',blank=True)
     
     
class CartItem(models.Model):
    user_id = models.IntegerField(null=True, blank=True) 
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    image = models.URLField() 
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.quantity}"
     
