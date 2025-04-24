from django.shortcuts import render,redirect
from item.models import Item, Category
from .forms import SignupForm
from django.contrib.auth import login

# Create your views here.
def index(request):
    items = Item.objects.filter(is_sold=False)[0:50]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {'items': items,
                                               'categories': categories})


def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})
