from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from decimal import Decimal
import random
from django.shortcuts import render
import string
from django.db import transaction
from django.db.models import Sum, F, DecimalField, ExpressionWrapper


from .models import Cart, CartItem, Monthly
from catalog.models import Product


@transaction.atomic
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_id = request.session['cart_id']

    if request.user.is_anonymous():
        cart, created = Cart.objects.get_or_create(cart_id=cart_id)
    elif request.user.is_authenticated():
        owner = request.user
        cart, created = Cart.objects.get_or_create(owner=owner, defaults={"cart_id": cart_id})

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(cart=cart, product=product)
        quantity = cart_item.quantity
        total = cart_item.total()
    else:
        cart_item.augment_quantity(1)
        quantity = cart_item.quantity
        total = cart_item.total()

    if request.user.is_anonymous():
        cart = Cart.objects.get(cart_id=cart_id)
    elif request.user.is_authenticated():
        cart = Cart.objects.get(owner=request.user)
    total_item = cart.items
    total_taka = cart.total

    return JsonResponse({"total_item": total_item, "total_taka": total_taka, "quantity": quantity, "total": total, "cart_item_id": cart_item.id, "cart_item_name": cart_item.name(), "cart_item_price": cart_item.price()})


@transaction.atomic
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_id = request.session['cart_id']
    if request.user.is_anonymous():
        cart = Cart.objects.get(cart_id=cart_id)
    elif request.user.is_authenticated():
        cart = Cart.objects.get(owner=request.user)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
    except CartItem.DoesNotExist:
        return JsonResponse({"msg": "Cannot remove. No item in cart."})
    else:
        if cart_item.quantity > 1:
            cart_item.augment_quantity(-1)
            quantity = cart_item.quantity
            total = cart_item.total()

            if request.user.is_anonymous():
                cart = Cart.objects.get(cart_id=cart_id)
            elif request.user.is_authenticated():
                cart = Cart.objects.get(owner=request.user)
            total_item = cart.items
            total_taka = cart.total

            return JsonResponse({"total_item": total_item, "total_taka": total_taka, "quantity": quantity, "total": total})
        else:
            return JsonResponse({"msg": "Cannot remove. Do you want to delete the item from your cart?"})


@transaction.atomic
def delete_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_id = request.session['cart_id']
    if request.user.is_anonymous():
        cart = Cart.objects.get(cart_id=cart_id)
    elif request.user.is_authenticated():
        cart = Cart.objects.get(owner=request.user)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
    except CartItem.DoesNotExist:
        return JsonResponse({"msg": "Item does not exist. No need to delete it."})
    else:
        id = cart_item.id
        cart_item.delete()

        if request.user.is_anonymous():
            cart = Cart.objects.get(cart_id=cart_id)
        elif request.user.is_authenticated():
            cart = Cart.objects.get(owner=request.user)
        total_item = cart.items
        total_taka = cart.total

        return JsonResponse({"item_id": id, "msg": "Deleted from cart", "total_item": total_item, "total_taka": total_taka})


def monthly_order(request):
    objs = Monthly.objects.filter(owner=request.user)
    total = objs.aggregate(
        total=ExpressionWrapper(
            Sum(F('product__price') * F('quantity')), output_field=DecimalField()))['total']
    if objs.exists():
        total = '%.2f' % total
    else:
        total = None
    return render(request, "cart/monthly-order.html", { "objs": objs, "total": total })


@transaction.atomic
def add_to_monthly(request, slug):
    product = get_object_or_404(Product, slug=slug)

    try:
        item = Monthly.objects.get(owner=request.user, product=product)
    except Monthly.DoesNotExist:
        item = Monthly.objects.create(owner=request.user, product=product)
        quantity = item.quantity
        total = item.total()
    else:
        item.augment_quantity(1)
        quantity = item.quantity
        total = item.total()
    objs = Monthly.objects.filter(owner=request.user)
    all_total = objs.aggregate(
        total=ExpressionWrapper(
            Sum(F('product__price') * F('quantity')), output_field=DecimalField()))['total']
    return JsonResponse({"id": item.id, "quantity": quantity, "total": total, "all_total": '%.2f' % all_total})


@transaction.atomic
def remove_from_monthly(request, slug):
    product = get_object_or_404(Product, slug=slug)

    try:
        item = Monthly.objects.get(owner=request.user, product=product)
    except Monthly.DoesNotExist:
        return JsonResponse({"message": "Item does not exist!"})
    else:
        if item.quantity > 1:
            item.augment_quantity(-1)
            quantity = item.quantity
            total = item.total()
            objs = Monthly.objects.filter(owner=request.user)
            all_total = objs.aggregate(
                total=ExpressionWrapper(
                    Sum(F('product__price') * F('quantity')), output_field=DecimalField()))['total']
        else:
            pass
        return JsonResponse({"id": item.id, "quantity": quantity, "total": total, "all_total": '%.2f' % all_total})


@transaction.atomic
def delete_from_monthly(request, slug):
    product = get_object_or_404(Product, slug=slug)

    try:
        item = Monthly.objects.get(owner=request.user, product=product)
    except Monthly.DoesNotExist:
        pass
    else:
        item_id = item.id
        item.delete()

    objs = Monthly.objects.filter(owner=request.user)
    all_total = objs.aggregate(
        total=ExpressionWrapper(
            Sum(F('product__price') * F('quantity')), output_field=DecimalField()))['total']
    return JsonResponse({"id": item_id, "all_total": all_total})


def transfer_order(request):
    monthly = Monthly.objects.filter(owner=request.user)

    for item in monthly:
        for i in range(item.quantity):
            add_to_cart(request, item.product.slug)

    cart = Cart.objects.get(owner=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    cart_array = []
    for item in cart_items:
        cart_array.append({'cart_item_id': item.id, 'item': item.product_id, 'price': item.product.price, 'name': item.product.name, 'qty': item.quantity, 'total': item.total(), 'slug': item.product.slug})

    return JsonResponse({'cart_items': cart.items, 'cart_total': cart.total, 'array': cart_array})

