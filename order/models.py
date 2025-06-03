

# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import User
from item.models import Item  # ton modèle d'article

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Commande #{self.id} de {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # prix unitaire au moment de la commande

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"
