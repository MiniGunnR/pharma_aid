import decimal
from django.db import models
from django.conf import settings
import datetime

from catalog.models import Product
from utils.models import TimeStamped


class Order(TimeStamped):
    # each individual status
    SUBMITTED = 1
    PROCESSED = 2
    DELIVERED = 3
    CANCELLED = 4
    RETURNED = 5

    # set of possible order statuses
    ORDER_STATUSES = ((SUBMITTED,'Submitted'),
                      (PROCESSED,'Processed'),
                      (DELIVERED,'Shipped'),
                      (CANCELLED,'Cancelled'),
                      (RETURNED,'Returned'),)

    # each individual payment method
    CASH_ON_DELIVERY = 1
    BKASH = 2

    # set of possible payment methods
    PAYMENT_METHODS = ((CASH_ON_DELIVERY,'Cash on Delivery'),
                       (BKASH,'bKash'),)

    # order info
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.GenericIPAddressField(auto_created=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    transaction_id = models.CharField(max_length=20, unique=True)

    # contact info
    email = models.EmailField(max_length=50)
    mobile = models.CharField(max_length=20)

    # shipping information
    shipping_name = models.CharField('Recipient Name', max_length=50)
    shipping_address_1 = models.CharField('Line 1', max_length=50)
    shipping_address_2 = models.CharField('Line 2', max_length=50, blank=True)
    shipping_city = models.CharField('City', max_length=50)
    shipping_zip = models.CharField('Zip Code', max_length=10)
    shipping_country = models.CharField('Country', max_length=50)

    # billing information
    billing_name = models.CharField(max_length=50)
    billing_address_1 = models.CharField(max_length=50)
    billing_address_2 = models.CharField(max_length=50, blank=True)
    billing_city = models.CharField(max_length=50)
    billing_zip = models.CharField(max_length=10)
    billing_country = models.CharField(max_length=50)

    delivery_date = models.CharField(max_length=50)

    # each individual delivery time
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6

    # set of possible delivery times
    DELIVERY_TIMES = ((ONE,'10AM - 12PM'),
                      (TWO,'12PM - 2PM'),
                      (THREE,'2PM - 4PM'),
                      (FOUR,'4PM - 6PM'),
                      (FIVE,'6PM - 8PM'),
                      (SIX,'8PM - 10PM'))

    delivery_time = models.IntegerField(choices=DELIVERY_TIMES, default=FOUR)
    delivery_charge = models.IntegerField(default=0)

    payment_method = models.IntegerField(choices=PAYMENT_METHODS, default=CASH_ON_DELIVERY)
    trx_id = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return 'Order #' + str(self.transaction_id)

    @property
    def subtotal(self):
        total = decimal.Decimal('0.00')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total

    @property
    def total(self):
        total = decimal.Decimal('0.00')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        total += self.delivery_charge
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=9,decimal_places=2)

    @property
    def total(self):
        return self.quantity * self.price

    @property
    def name(self):
        return self.product.name

    @property
    def sku(self):
        return self.product.sku

    def __unicode__(self):
        return self.product.name + ' (' + self.product.sku + ')'

    def get_absolute_url(self):
        return self.product.get_absolute_url()


REQUESTED = 1
PROCESSING = 2
DELIVERED = 3

class RequestedProduct(TimeStamped):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=100, blank=True)
    power = models.CharField(max_length=100, blank=True)
    quantity = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)

    status_choices = (
        (REQUESTED, 'Requested'),
        (PROCESSING, 'Processing'),
        (DELIVERED, 'Delivered'),
    )

    status = models.SmallIntegerField(choices=status_choices,
                                      default=REQUESTED)
    note = models.CharField(max_length=255, default='')

    def __unicode__(self):
        return self.name


class Prescription(TimeStamped):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # image = models.ImageField(upload_to='static/img/uploads/prescription', height_field='height', width_field='width')
    image = models.ImageField(upload_to='img/prescription', height_field='height', width_field='width')
    # thumbnail = models.ImageField(upload_to='static/img/uploads/prescription')
    thumbnail = models.ImageField(upload_to='img/prescription')
    height = models.PositiveIntegerField(blank=True, null=True)
    width = models.PositiveIntegerField(blank=True, null=True)


    def __unicode__(self):
        return "{0} - {1}".format(self.user, self.id)

    def create_thumbnail(self):
        if not self.image:
            return

        from PIL import Image
        from io import BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        THUMBNAIL_SIZE = (200,200)

        DJANGO_TYPE = self.image.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'

        image = Image.open(BytesIO(self.image.read()))

        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
            temp_handle.read(), content_type=DJANGO_TYPE)

        self.thumbnail.save('{0}_thumbnail.{1}'.format(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)

    def save(self, *args, **kwargs):
        self.create_thumbnail()
        super(Prescription, self).save(*args, **kwargs)
