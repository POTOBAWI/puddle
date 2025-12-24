from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('/')

def home_redirect(request):
    return redirect('core:index')  

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('core.urls')), 
    path('items/', include("item.urls")),
    path('inbox/', include("conversation.urls")),
    path('dashboard/', include('dashboard.urls')),
    path('cart/', include('cart.urls')),
    path('logout/', custom_logout, name='logout'),
)
# chemins hors i18n
urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),  # pour changer la langue
    path('', home_redirect, name="home_redirect"),    # racine si nécessaire
]
