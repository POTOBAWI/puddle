from django.urls import path

from . import views

from django.urls import path
from . import views

app_name = 'conversation'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('new/<int:item_pk>/', views.new_conversation, name='new'),  # / ajouté
    path('<int:pk>/', views.detail, name='detail'),                  # / ajouté
    path("traduire/", views.traducteur_vue, name="traduire_vue"),
    path("resumer/", views.summarize_view, name="resumer"),
]
