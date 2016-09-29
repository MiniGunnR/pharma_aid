from django.db import models
from django.utils.text import slugify
import random

from utils.models import TimeStamped


class Category(TimeStamped):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, help_text='Unique value for product page URL, created from name.')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords", max_length=255, blank=True, help_text='Comma-delimited set of SEO keywords for meta tag.')
    meta_description = models.CharField("Meta Description", max_length=255, blank=True, help_text='Content for description meta tag.')

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self. name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('catalog:category', kwargs={ "category_slug": self.slug })


class Manufacturer(TimeStamped):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(TimeStamped):
    # each individual dosage assignment
    TABLET = 1
    CAPSULE = 2
    SUPPOSITORY = 3
    SYRUP = 4
    SUSPENSION = 5
    INJECTION_IV = 6
    INJECTION_IM = 7
    CONTRACEPTIVE = 8
    SANITARY_NAPKIN = 9
    CREAM = 10
    OINTMENT = 11

    # set of possible dosage types
    DOSAGE_TYPES = (
        (TABLET, 'Tablet'),
        (CAPSULE, 'Capsule'),
        (SUPPOSITORY, 'Suppository'),
        (SYRUP, 'Syrup'),
        (SUSPENSION, 'Suspension'),
        (INJECTION_IV, 'Injection (IV)'),
        (INJECTION_IM, 'Injection (IM)'),
        (CONTRACEPTIVE, 'Contraceptive'),
        (SANITARY_NAPKIN, 'Sanitary Napkin'),
        (CREAM, 'Cream'),
        (OINTMENT, 'Ointment'),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, help_text='Unique value for product page URL, created from name.')
    generic = models.CharField(max_length=50, blank=True)
    power = models.CharField(max_length=50, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True)
    sku = models.CharField(max_length=50, blank=True, help_text='Unique identifier for the product')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00)
    is_active = models.BooleanField(default=True, help_text='Deselect this instead of deleting the product.')
    unit = models.CharField(max_length=20, default='piece', help_text='Unit used to sell the product, e.g. 250 gm, bottle, etc.')
    description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField("Meta Keywords", max_length=255, blank=True, help_text='Comma-delimited set of SEO keywords for meta tag.')
    meta_description = models.CharField("Meta Description", max_length=255, blank=True, help_text='Content for description meta tag.')
    category = models.ForeignKey(Category)

    dosage = models.PositiveIntegerField(choices=DOSAGE_TYPES,
                                         default=TABLET)

    class Meta:
        db_table = 'products'
        ordering = ['-created']

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('catalog_product', (), { 'product_slug': self.slug })

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    def display_name(self):
        if (self.dosage == self.TABLET) or (self.dosage == self.SUPPOSITORY):
            return "{0} {1} {2}".format(self.name, self.power, self.get_dosage_display())
        if self.dosage == self.SYRUP:
            return "{0} {1} {2} Bottle".format(self.name, self.get_dosage_display(), self.power)
        if (self.dosage == self.CREAM) or (self.dosage == self.OINTMENT):
            return "{0} {1} {2} Tube".format(self.name, self.get_dosage_display(), self.power)
        else:
            return "{0} {1} {2}".format(self.name, self.power, self.get_dosage_display())

    def save(self, *args, **kwargs):
        # self.slug = slugify("{0}-{1}-{2}".format(self.name, self.dosage, self.power))
        self.slug = slugify("{0}-{1}-{2}".format(self.name, self.dosage, str(random.random())))
        super(Product, self).save(*args, **kwargs)
