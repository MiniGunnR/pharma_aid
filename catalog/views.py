from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.core import serializers
from django.db import IntegrityError
from django.db.models import Q

import csv
from django.conf import settings
from django.utils.text import slugify

from .models import Category, Product, SubCategory, Manufacturer, Dosage


def index(request):
    # category = Category.objects.all().first()
    # return HttpResponseRedirect(reverse('catalog:category', args=[category.slug]))
    return HttpResponseRedirect('/category/medicine/')


def more_items(request, category_slug):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()[200:]
    response = serializers.serialize('json', products, fields=('name', 'price', 'slug'))
    return HttpResponse(response, content_type="application/json")


def show_category(request, category_slug):
    c = get_object_or_404(Category, slug=category_slug)

    products = c.product_set.all()[:200]

    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render(request, "catalog/category.html", locals())


def show_subcategory(request, category_slug, subcategory_slug):
    c = get_object_or_404(Category, slug=category_slug)
    s = get_object_or_404(SubCategory, slug=subcategory_slug)

    products = s.product_set.all()[:200]

    page_title = s.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render(request, "catalog/subcategory.html", locals())


def show_product(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    return render(request, "catalog/show_product.html", { "product": product })


def search_products(request):
    query = request.GET['search']
    products = Product.objects.filter(name__icontains=query) | Product.objects.filter(generic__icontains=query)
    return render(request, "catalog/search-result.html", {"products": products})


def auto(request):
    file = open("{0}{1}{2}".format(settings.BASE_DIR, '/', '1.csv'))
    reader = csv.reader(file)
    data = list(reader)
    for datum in data:
        category, created = Category.objects.get_or_create(name=datum[8])

        try:
            subcategory, created = SubCategory.objects.get_or_create(name=datum[10], category=category)
        except IntegrityError as e:
            subcategory = None

        manufacturer, created = Manufacturer.objects.get_or_create(name=datum[2])

        try:
            dosage, created = Dosage.objects.get_or_create(name=datum[7])
        except IntegrityError as e:
            dosage = None

        if datum[3] == "":
            price = 0.0
        else:
            price = datum[3]

        try:
            Product.objects.create(name=datum[0], generic=datum[1], manufacturer=manufacturer, price=price, is_active=datum[11], unit=datum[5], dosage=dosage, category=category, subcategory=subcategory)
        except IntegrityError as e:
            pass
        except ValidationError as e:
            pass

    return HttpResponseRedirect('/')

