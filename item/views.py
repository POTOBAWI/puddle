from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Item,Category
from .forms import NewItemForm,EditItemForm
from django.db.models import Q
from .models import ItemView
from .utils import get_recommendations_for_user


# Create your views here.
def items(request):
    print(">>> items view called")
    query=request.GET.get('query','')
    items=Item.objects.filter(is_sold=False)
    category_id=request.GET.get('category',0)
    categories=Category.objects.all()
    recommendations = []
    if request.user.is_authenticated:
        print(">>> Utilisateur connecté :", request.user)
        recommendations = get_recommendations_for_user(request.user)

    if query:
        items=items.filter(Q(name__icontains=query )| Q(description__icontains=query))
    return render(request,'item/items.html',{'items':items,'categories':categories,'category_id':int(category_id),'recommendations': recommendations})


def detail(request,pk):
    item=get_object_or_404(Item,pk=pk)
    related_items=Item.objects.filter(category=item.category,is_sold=False).exclude(pk=pk).order_by('-created_at')
    if not ItemView.objects.filter(user=request.user, item=item).exists():
        # If the item has not been viewed by the user, create a new ItemView
        viewedItem=ItemView.objects.create(user=request.user, item=item)
    return render (request,'item/detail.html',{'item':item,'related_items':related_items})






  
    

    


@login_required
def newItem(request):
    if request.method== 'POST':
        form=NewItemForm(request.POST,request.FILES)
        if form.is_valid():
            item =form.save(commit=False)
            item.created_by=request.user
            item.save()
            return redirect('item:detail',pk=item.id)
    else:
        form=NewItemForm()
    return render(request,'item/form.html',{
        'form':form,
        'title':'New Item'
    })

@login_required
def edit(request,pk):
    item=get_object_or_404(Item,pk=pk,created_by=request.user)
    if request.method== 'POST':
        form=EditItemForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
           
           form.save()
           return redirect('item:detail',pk=item.id)
    else:
        form=EditItemForm(instance=item)
    return render(request,'item/form.html',{
        'form':form,
        'title':'New Item'
    })

def delete(request,pk):
    item=get_object_or_404(Item,pk=pk,created_by=request.user)
    item.delete()

    return redirect('dashboard:index')
