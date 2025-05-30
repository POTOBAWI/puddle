from .models import ItemView, Item
from django.db.models import Count
from django.db.models import Q


 

from .models import ItemView, Item
from django.db.models import Count

def get_recommendations_for_user(user, limit=5):
    viewed_items = ItemView.objects.filter(user=user).values_list('item__category', flat=True).distinct()

    recommended_items = Item.objects.filter(category_id__in=viewed_items)\
        .exclude(itemview__user=user)\
        .exclude(created_by=user)\
        .annotate(num_views=Count('itemview'))\
        .order_by('-num_views')[:limit]

    return recommended_items
