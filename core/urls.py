from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm


app_name = 'core'

urlpatterns = [
    path('',views.index,name='index'),
    
    path('contact/',views.contact,name='contact'),
   path('signup/',views.signup,name='signup'),
   path('login/',auth_views.LoginView.as_view(template_name="core/login.html",authentication_form=LoginForm),name="login"),
   path('changer_langue/', views.changer_langue, name='changer_langue'),
   path('noter_vendeur/<int:vendeur_id>/<int:item_id>', views.noter_vendeur, name='noter_vendeur'),

    
]
