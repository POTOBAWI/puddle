from django.urls import path

from . import views

from django.urls import path
from . import views

app_name = 'conversation'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('new/<int:item_pk>/', views.new_conversation, name='new'),  # / ajouté
    path('<int:pk>/', views.detail, name='detail'),                  # / ajouté
    
]
