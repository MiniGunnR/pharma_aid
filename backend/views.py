from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from act.models import User
from catalog.models import Category, Product, Manufacturer
from order.models import RequestedProduct, Order, Prescription, OrderItem
from utils.models import Misc


@login_required
def dashboard(request):
    return render(request, "backend/dashboard.html")


@login_required
def items(request):
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "backend/items.html", context)


class ItemDetailView(DetailView):
    model = Product
    template_name = "backend/item-detail.html"


class ItemUpdateView(UpdateView):
    model = Product
    fields = ['name', 'generic', 'power', 'manufacturer', 'sku', 'price', 'is_active', 'unit', 'description', 'meta_keywords', 'meta_description', 'category', 'dosage']
    template_name = "backend/item-form.html"
    success_url = '../../'


class ItemCreateView(CreateView):
    model = Product
    fields = ['name', 'generic', 'power', 'manufacturer', 'sku', 'price', 'is_active', 'unit', 'description', 'meta_keywords', 'meta_description', 'category', 'dosage']
    template_name = "backend/item-form.html"
    success_url = '/backend/items/'


@login_required
def manufacturers(request):
    manufacturers = Manufacturer.objects.all()
    context = {
        "manufacturers": manufacturers,
    }
    return render(request, "backend/manufacturers.html", context)


class ManufacturerCreateView(CreateView):
    model = Manufacturer
    fields = ['name']
    template_name = "backend/manufacturer-form.html"
    success_url = '/backend/manufacturers/'


class ManufacturerItemsListView(ListView):
    model = Product
    template_name = "backend/manufacturer-items.html"

    def get_context_data(self, **kwargs):
        context = super(ManufacturerItemsListView, self).get_context_data()
        context['manufacturer'] = Manufacturer.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        manufacturer = Manufacturer.objects.get(slug=self.kwargs['slug'])
        return Product.objects.filter(manufacturer=manufacturer)

@login_required
def categories(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, "backend/categories.html", context)


class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'description', 'is_active', 'meta_keywords', 'meta_description']
    template_name = "backend/category-form.html"
    success_url = '/backend/categories/'


class CategoryItemsListView(ListView):
    model = Product
    template_name = "backend/category-items.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryItemsListView, self).get_context_data()
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return Product.objects.filter(category=category)


@login_required
def requested_products(request):
    requested_products = RequestedProduct.objects.all().order_by('-created')
    context = {
        "requested_products": requested_products,
    }
    return render(request, "backend/requested_products.html", context)


class RequestedProductDetailView(DetailView):
    model = RequestedProduct
    template_name = "backend/requested_products_detailview.html"


@login_required
def orders(request):
    orders = Order.objects.all().order_by('-created')
    context = {
        "orders": orders,
    }
    return render(request, "backend/orders.html", context)


class OrderDetailView(DetailView):
    model = Order
    template_name = "backend/order-detail.html"

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data()
        context['items'] = OrderItem.objects.filter(order=self.object)
        return context

@login_required
def prescriptions(request):
    prescriptions = Prescription.objects.all()
    context = {
        "prescriptions": prescriptions,
    }
    return render(request, "backend/prescription.html", context)

@login_required
def Users(request):
    users = User.objects.all()
    context = {
        "users": users,
    }
    return render(request, "backend/users.html", context)


@login_required
def MiscView(request):
    misc = Misc.objects.all()
    context = {
        "misc": misc,
    }
    return render(request, "backend/misc.html", context)


class MiscSettingsUpdateView(UpdateView):
    model = Misc
    fields = ['value']
    template_name = "backend/misc-form.html"
    success_url = '/backend/misc/settings/'

