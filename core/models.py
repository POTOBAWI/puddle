from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from item.models import Item

class Profile(models.Model):
    LANGUE_CHOICES = [
        ('fr', 'Français'),
        ('en', 'English'),
        
        # Ajoute d’autres langues si nécessaire
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    langue = models.CharField(max_length=2, choices=LANGUE_CHOICES, default='fr')

    def __str__(self):
        return f"{self.user.username} - {self.langue}"



    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


class SellerRating(models.Model):
    vendeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes_recues")
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes_donnees")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # l’item vendu
    note = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    commentaire = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('vendeur', 'client', 'item')  # pas deux notes pour le même achat

    def __str__(self):
        return f"{self.vendeur.username} {self.note}★ par {self.client.username}"

