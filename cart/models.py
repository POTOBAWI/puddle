from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from item.models import Item

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')  # empêche les doublons

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"

