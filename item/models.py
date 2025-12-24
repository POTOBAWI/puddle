from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(_("Nom de la catégorie"), max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Catégories")

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, verbose_name=_("Catégorie"), on_delete=models.CASCADE)
    name = models.CharField(_("Nom"), max_length=255)   
    description = models.TextField(_("Description"), blank=True, null=True)
    price = models.DecimalField(_("Prix"), max_digits=10, decimal_places=2)
    image = models.ImageField(_("Image"), upload_to='item_images', blank=True, null=True)  
    is_sold = models.BooleanField(_("Vendu"), default=False)
    created_by = models.ForeignKey(User, verbose_name=_("Utilisateur"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    location=models.CharField(max_length=255, verbose_name=_("Emplacement"), blank=True, null=True,default='Lomé')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def __str__(self):
        return self.name
# classe pour recupérer les articles vus par un utilisateur
class ItemView(models.Model):
    user = models.ForeignKey(User, verbose_name=_("Utilisateur"), on_delete=models.CASCADE)
    item = models.ForeignKey('Item', verbose_name=_("Article"), on_delete=models.CASCADE, related_name="itemviews")
    viewed_at = models.DateTimeField(_("Vu le"), auto_now_add=True)
