from django.db import models
from django.utils.text import slugify
import random
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible
from django.conf import settings
from .storage import OverwriteStorage

from utils.models import TimeStamped


class Category(TimeStamped):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, help_text='Unique value for product page URL, created from name.')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords", max_length=255, blank=True, help_text='Comma-delimited set of SEO keywords for meta tag.')
    meta_description = models.CharField("Meta Description", max_length=255, blank=True, help_text='Content for description meta tag.')
    image = models.ImageField(upload_to='img/category', blank=True)

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self. name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('catalog:category', kwargs={ "category_slug": self.slug })


class SubCategory(TimeStamped):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, help_text='Unique value for product page URL, created from name.')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'sub_categories'
        ordering = ['name']
        verbose_name_plural = 'Sub-Categories'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('catalog:show_subcategory', kwargs={ "category_slug": self.category.slug, "subcategory_slug": self.slug })


class Manufacturer(TimeStamped):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Manufacturer, self).save(*args, **kwargs)


class Dosage(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Dosage, self).save(*args, **kwargs)


@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.slug:
            filename = '{}.{}'.format(instance.slug, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)


@deconstructible
class UploadToPathAndRenameThumbnail(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.slug:
            filename = '{}_thumbnail.{}'.format(instance.slug, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)


class Product(TimeStamped):
    # each individual dosage assignment
    # TABLET = 1
    # CAPSULE = 2
    # SUPPOSITORY = 3
    # SYRUP = 4
    # SUSPENSION = 5
    # INJECTION_IV = 6
    # INJECTION_IM = 7
    # CONTRACEPTIVE = 8
    # SANITARY_NAPKIN = 9
    # CREAM = 10
    # OINTMENT = 11
    # BLANK = 12

    # set of possible dosage types
    # DOSAGE_TYPES = (
    #     (TABLET, 'Tablet'),
    #     (CAPSULE, 'Capsule'),
    #     (SUPPOSITORY, 'Suppository'),
    #     (SYRUP, 'Syrup'),
    #     (SUSPENSION, 'Suspension'),
    #     (INJECTION_IV, 'Injection (IV)'),
    #     (INJECTION_IM, 'Injection (IM)'),
    #     (CONTRACEPTIVE, 'Contraceptive'),
    #     (SANITARY_NAPKIN, 'Sanitary Napkin'),
    #     (CREAM, 'Cream'),
    #     (OINTMENT, 'Ointment'),
    #     (BLANK, ''),
    # )

    name = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, help_text='Unique value for product page URL, created from name.')
    generic = models.CharField(max_length=400, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00)
    is_active = models.BooleanField(default=True, help_text='Deselect this instead of deleting the product.')
    unit = models.CharField(max_length=100, default='Piece', help_text='Unit used to sell the product, e.g. 250 gm, bottle, etc.')
    description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField("Meta Keywords", max_length=255, blank=True, help_text='Comma-delimited set of SEO keywords for meta tag.')
    meta_description = models.CharField("Meta Description", max_length=255, blank=True, help_text='Content for description meta tag.')
    category = models.ForeignKey(Category)
    subcategory = models.ForeignKey(SubCategory, blank=True, null=True)
    related = models.ManyToManyField("self", blank=True)

    height = models.CharField(max_length=4, blank=True, null=True)
    width = models.CharField(max_length=4, blank=True, null=True)
    image = models.ImageField(upload_to=UploadToPathAndRename('img/items'), height_field='height', width_field='width', blank=True, storage=OverwriteStorage())
    thumbnail = models.ImageField(upload_to=UploadToPathAndRenameThumbnail('img/items'), height_field='height', width_field='width', blank=True, storage=OverwriteStorage())

    # dosage = models.PositiveIntegerField(choices=DOSAGE_TYPES,
    #                                      default=TABLET)
    dosage = models.ForeignKey(Dosage, blank=True, null=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('catalog_product', (), { 'product_slug': self.slug })

    def current_price(self):
        if self.discount_price > 0:
            return self.discount_price
        else:
            return self.price

    def sale_price(self):
        if self.discount_price > 0:
            return "%s <small><strike>Tk. %s</strike></small>" % (self.discount_price, self.price)
        else:
            return self.price

    def display_name(self):
        if (self.dosage == self.TABLET) or (self.dosage == self.SUPPOSITORY):
            return "{0} {1} {2}".format(self.name, self.power, self.get_dosage_display())
        if self.dosage == self.SYRUP:
            return "{0} {1} {2} Bottle".format(self.name, self.get_dosage_display(), self.power)
        if (self.dosage == self.CREAM) or (self.dosage == self.OINTMENT):
            return "{0} {1} {2} Tube".format(self.name, self.get_dosage_display(), self.power)
        else:
            return "{0} {1} {2}".format(self.name, self.power, self.get_dosage_display())

    def create_thumbnail(self):
        if not self.image:
            return

        from PIL import Image
        try:
            from cStringIO import StringIO
        except:
            from StringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        THUMBNAIL_SIZE = (130,130)

        # DJANGO_TYPE = self.image.file.content_type
        # The following is added because 'File' object has no attribute 'content_type' error is displayed
        if self.image.name.endswith(".jpg"):
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
            DJANGO_TYPE = 'image/jpeg'

        elif self.image.name.endswith(".png"):
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
            DJANGO_TYPE = 'image/png'
        # End of content_type alternative code

        # if DJANGO_TYPE == 'image/jpeg':
        #     PIL_TYPE = 'jpeg'
        #     FILE_EXTENSION = 'jpg'
        # elif DJANGO_TYPE == 'image/png':
        #     PIL_TYPE = 'png'
        #     FILE_EXTENSION = 'png'

        image = Image.open(StringIO(self.image.read()))

        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)

        self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)

    def save(self, *args, **kwargs):
        # self.slug = slugify("{0}-{1}-{2}".format(self.name, self.dosage, str(int(random.random() * 1000000))))
        self.slug = slugify("{0}-{1}".format(self.name, self.dosage))
        if self.image is not None:
            try:
                prod = Product.objects.get(pk=self.pk)
            except Product.DoesNotExist:
                pass
            else:
                original_image = prod.image
            if 'original_image' in locals():
                if original_image != self.image:
                    self.create_thumbnail()
            return super(Product, self).save(*args, **kwargs)

