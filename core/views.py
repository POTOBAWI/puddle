from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils import translation

from item.models import Item, Category
from item.utils import get_recommendations_for_user
from .models import SellerRating
from .forms import ProfileForm, SellerRatingForm, SignupForm


@login_required
def index(request):
    items = Item.objects.filter(is_sold=False)[:50]
    categories = Category.objects.all()
    recommendations = get_recommendations_for_user(request.user)

    return render(request, 'core/index.html', {
        'items': items,
        'categories': categories,
        'recommendations': recommendations
    })


def contact(request):
    return render(request, 'core/contact.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})


@login_required
def changer_langue(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            langue = form.cleaned_data['langue']

            profile = request.user.profile
            profile.langue = langue
            profile.save()

            translation.activate(langue)
            request.session["django_language"] = langue

            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = ProfileForm(initial={'langue': request.user.profile.langue})

    return render(request, 'core/changer_langue.html', {'form': form})


@login_required
def noter_vendeur(request, item_id, vendeur_id):
    item = get_object_or_404(Item, id=item_id)
    vendeur = get_object_or_404(User, id=vendeur_id)

    note_existante = SellerRating.objects.filter(
        vendeur=vendeur,
        client=request.user,
        item=item
    ).first()

    if request.method == "POST":
        form = SellerRatingForm(request.POST, instance=note_existante)
        if form.is_valid():
            note = form.save(commit=False)
            note.vendeur = vendeur
            note.client = request.user
            note.item = item
            note.save()
            return redirect("item:detail", pk=item.id)
    else:
        form = SellerRatingForm(instance=note_existante)

    return render(request, "core/noter_vendeur.html", {
        "form": form,
        "vendeur": vendeur,
        "item": item
    })
