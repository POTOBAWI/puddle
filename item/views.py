from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Item,Category
from .forms import NewItemForm,EditItemForm
from django.db.models import Q
from .models import ItemView

from .utils import get_recommendations_for_user
from django.contrib import messages

from core.utils import translate, summarize_text,moyenne_notes


# Create your views here.
def items(request):
   
    query=request.GET.get('query','')
    items=Item.objects.filter(is_sold=False)
    
    category_id=request.GET.get('category',0)
    
    categories=Category.objects.all()
 
       
    recommendations = get_recommendations_for_user(request.user)

    if query:
        items=items.filter(Q(name__icontains=query )| Q(description__icontains=query )| Q(category__name__icontains=query))
    return render(request,'item/items.html',{'items':items,'categories':categories,'category_id':int(category_id),'recommendations': recommendations})

@login_required
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    note=moyenne_notes(item.created_by)
    related_items = Item.objects.filter(
        category=item.category, is_sold=False
    ).exclude(pk=pk).order_by('-created_at')

    # Supposons que toutes tes descriptions sont en FR
    user_lang = getattr(request.user.profile, "langue", "fr")

    if user_lang == "en":
        desc_traduite = translate(item.description, target_lang="en", source_lang="fr")
    else:
        desc_traduite = item.description

    desc_reduite = summarize_text(desc_traduite)

    if not ItemView.objects.filter(user=request.user, item=item).exists():
        ItemView.objects.create(user=request.user, item=item)

    return render(
        request,
        "item/detail.html",
        {"item": item, "related_items": related_items, "desc_reduite": desc_reduite,"note": note},
    )


@login_required
def category_items(request,pk):
    category=get_object_or_404(Category,pk=pk)
    items=Item.objects.filter(category=category).order_by('-created_at')
    for item in items:
        lang = request.user.profile.langue
        item.trans_fields = [translate(item.name, lang), translate(item.description, lang)]

    return render(request,'item/items.html',{'items':items})






  
    

    


@login_required
def newItem(request):
    if request.method== 'POST':
        form=NewItemForm(request.POST,request.FILES)
        if form.is_valid():
            item =form.save(commit=False)
            item.created_by=request.user        
            messages.success(request, 'votre article est créé avec succés.')

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



