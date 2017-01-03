from django.db import models
from django.conf import settings

from catalog.models import Product
from utils.models import TimeStamped


class Cart(TimeStamped):
    cart_id = models.CharField(max_length=50)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    items = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'cart_owners'
        ordering = ['created']

    def __str__(self):
        return self.cart_id


class CartItem(TimeStamped):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey('catalog.Product', unique=False)

    class Meta:
        db_table = 'cart_items'
        ordering = ['created']

    def __init__(self, *args, **kwargs):
        super(CartItem, self).__init__(*args, **kwargs)
        self.__important_fields = ['quantity']
        for field in self.__important_fields:
            setattr(self, '__original_%s' % field, getattr(self, field))

    def has_increased(self):
        for field in self.__important_fields:
            orig = '__original_%s' % field
            if getattr(self, orig) < getattr(self, field):
                return True
        return False

    def has_decreased(self):
        for field in self.__important_fields:
            orig = '__original_%s' % field
            if getattr(self, orig) > getattr(self, field):
                return True
        return False

    def total(self):
        return self.quantity * self.product.current_price()

    def name(self):
        return self.product.name

    def price(self):
        return self.product.current_price()

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def augment_quantity(self, quantity):
        self.quantity = self.quantity + int(quantity)
        self.save()

    def __unicode__(self):
        return "{0} - {1}".format(self.cart_id, self.product.name)


class Monthly(TimeStamped):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey('catalog.Product', unique=False)
    quantity = models.PositiveIntegerField(default=1)

    def total(self):
        return self.quantity * self.product.price

    def name(self):
        return self.product.name

    def price(self):
        return self.product.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def augment_quantity(self, quantity):
        self.quantity = self.quantity + int(quantity)
        self.save()

    def __unicode__(self):
        return self.owner.name
