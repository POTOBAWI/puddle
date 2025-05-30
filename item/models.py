from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural= 'Categories'
    def __str__(self):
        return self.name
class Item(models.Model):
    category=models.ForeignKey(Category,verbose_name='items',on_delete=models.CASCADE)
    name=models.CharField(max_length=255)   
    description=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='item_images',blank=True,null=True)  
    is_sold=models.BooleanField(default=False)
    created_by=models.ForeignKey(User, verbose_name='Users', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-created_at',)
    def __str__(self):
        return self.name
    


class ItemView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

 