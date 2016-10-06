from catalog.models import Category, SubCategory
from cart.models import Cart, CartItem

from django.conf import settings

import random
import string


def pharma_aid(request):
    # Set the cart_id
    if 'cart_id' not in request.session:
        request.session['cart_id'] = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(50))

    try:
        if request.user.is_anonymous():
            cart = Cart.objects.get(cart_id=request.session['cart_id'])
        elif request.user.is_authenticated():
            cart = Cart.objects.get(owner=request.user)
    except Cart.DoesNotExist:
        total_item = total_taka = 0
        big_bag_items = []
    else:
        total_item = cart.items
        total_taka = cart.total
        big_bag_items = cart.cartitem_set.all()

    return {
        'total_item': total_item,
        'total_taka': total_taka,
        'big_bag_items': big_bag_items,
        'active_categories': Category.objects.filter(is_active=True),
        'active_sub_categories': SubCategory.objects.filter(is_active=True),
        'site_name': settings.SITE_NAME,
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION,
        'request': request
    }
