from django.db.models.signals import post_save, post_delete
from allauth.account.signals import user_logged_in
from collections import Counter

from django.dispatch import receiver
from cart.models import Cart, CartItem
from catalog.models import Product


@receiver(post_save, sender=CartItem)
def adjust_item_add_edit(instance, created, **kwargs):
    cart = instance.cart
    if created:
        cart.items += 1
        cart.total = float(cart.total) + float(instance.price())
        cart.save()
    if not created:
        if instance.has_increased():
            cart.total = float(cart.total) + float(instance.price())
            cart.save()
        elif instance.has_decreased():
            cart.total = float(cart.total) - float(instance.price())
            cart.save()


@receiver(post_delete, sender=CartItem)
def adjust_item_delete(instance, **kwargs):
    cart = instance.cart
    cart.items -= 1
    cart.total -= instance.total()
    cart.save()


def _anon_cart_items(request):
    try:
        anon_cart = Cart.objects.get(cart_id=request.session['cart_id'])
    except Cart.DoesNotExist:
        items = {}
    else:
        items = anon_cart.cartitem_set.all()
    anon_dict = {item.product.id: item.quantity for item in items}
    return Counter(anon_dict)


def _auth_cart_items(request):
    try:
        auth_cart = Cart.objects.get(owner=request.user)
    except Cart.DoesNotExist:
        items = []
        auth_dict = {}
    else:
        items = auth_cart.cartitem_set.all()
        auth_dict = {item.product_id: item.quantity for item in items}
    return Counter(auth_dict)


@receiver(user_logged_in)
def merge_carts(request, user, **kwargs):
    anon_cart_items_num = _anon_cart_items(request)
    auth_cart_items_num = _auth_cart_items(request)
    final_cart_items_num = dict(anon_cart_items_num + auth_cart_items_num)

    # Delete the anonymous cart
    try:
        anon_cart = Cart.objects.get(cart_id=request.session['cart_id'])
    except Cart.DoesNotExist:
        pass
    else:
        anon_cart.delete()

    # Clear the auth cart
    try:
        auth_cart = Cart.objects.get(owner=request.user)
    except Cart.DoesNotExist:
        auth_cart = Cart.objects.create(cart_id=request.session['cart_id'], owner=request.user)
    else:
        auth_items = auth_cart.cartitem_set.all()
        for item in auth_items:
            item.delete()

    # Save items in auth cart
    total_taka = 0
    for prod_id, qty in final_cart_items_num.items():
        product = Product.objects.get(id=prod_id)
        cart_item = CartItem.objects.create(cart=auth_cart, quantity=qty, product=product)
        total_taka += cart_item.total()

    auth_cart.total = total_taka
    auth_cart.save()
