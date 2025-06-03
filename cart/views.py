

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem
from item.models import Item
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from order.models import Order, OrderItem

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart:view_cart')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum([ci.item.price * ci.quantity for ci in cart_items])
    return render(request, 'cart/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, user=request.user, item_id=item_id)
    cart_item.delete()
    return JsonResponse({'success': True})



@csrf_exempt  # si tu veux éviter ça, passe le token depuis Vue.js comme déjà montré
@login_required
def update_quantity(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))

            cart_item = CartItem.objects.get(user=request.user, item_id=item_id)
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({'success': True, 'quantity': cart_item.quantity})
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found in cart.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)



@login_required
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.item.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        # 1. Créer l'objet Order
        order = Order.objects.create(
            user=request.user,
            total_price=total
        )

        # 2. Créer les OrderItem
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                item=item.item,
                quantity=item.quantity,
                price=item.item.price
            )

        # 3. Vider le panier
        cart_items.delete()

        # 4. Rediriger vers une page de confirmation
        return redirect('cart:confirm_order')

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })
def confirm_order(request):
    return render(request, 'cart/confirm_order.html')


