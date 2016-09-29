from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page

import csv
from django.conf import settings
from django.utils.text import slugify

from .models import Category, Product


def index(request):
    # category = Category.objects.all().first()
    # return HttpResponseRedirect(reverse('catalog:category', args=[category.slug]))
    return HttpResponseRedirect('/category/medicine/')


@cache_page(60 * 15)
def show_category(request, category_slug):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render(request, "catalog/category.html", locals())


def show_product(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    return render(request, "catalog/show_product.html", { "product": product })


def search_products(request):
    query = request.GET['search']
    products = Product.objects.filter(name__icontains=query)
    return render(request, "catalog/search-result.html", {"products": products})


def auto(request):
    file = open("{0}{1}{2}".format(settings.BASE_DIR, '/', '1.csv'))
    reader = csv.reader(file)
    data = list(reader)
    # cat = Category.objects.get(slug='tablet')
    for datum in data:
        category, created = Category.objects.get_or_create(name=datum[2])
        prod = Product.objects.create(name=datum[0], price=datum[1], category=category)
        # prod.categories.add(cat)
    return HttpResponseRedirect('/')
