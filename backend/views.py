from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from act.models import User, Address, AddressInfo
from catalog.models import Category, Product, Manufacturer, SubCategory
from order.models import RequestedProduct, Order, Prescription, OrderItem
from utils.models import Misc


@staff_member_required
def dashboard(request):
    return render(request, "backend/dashboard.html")


@staff_member_required
def items(request):
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "backend/items.html", context)


class ItemDetailView(DetailView):
    model = Product
    template_name = "backend/item-detail.html"

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(ItemDetailView, self).dispatch(*args, **kwargs)


class ItemUpdateView(UpdateView):
    model = Product
    fields = ['name', 'generic', 'manufacturer', 'price', 'discount_price', 'image', 'is_active', 'unit', 'description', 'meta_keywords', 'meta_description', 'category', 'dosage']
    template_name = "backend/item-form.html"
    success_url = '../../'

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(ItemUpdateView, self).dispatch(*args, **kwargs)


class ItemCreateView(CreateView):
    model = Product
    fields = ['name', 'generic', 'manufacturer', 'price', 'image', 'is_active', 'unit', 'description', 'meta_keywords', 'meta_description', 'category', 'dosage']
    template_name = "backend/item-form.html"
    success_url = '/backend/items/'

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(ItemCreateView, self).dispatch(*args, **kwargs)


@staff_member_required
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

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(ManufacturerCreateView, self).dispatch(*args, **kwargs)


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

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(ManufacturerItemsListView, self).dispatch(*args, **kwargs)

@staff_member_required
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

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(CategoryCreateView, self).dispatch(*args, **kwargs)


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

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(CategoryItemsListView, self).dispatch(*args, **kwargs)


class SubCategoryItemsListView(ListView):
    model = Product
    template_name = "backend/subcategory-items.html"

    def get_context_data(self, **kwargs):
        context = super(SubCategoryItemsListView, self).get_context_data()
        context['subcategory'] = SubCategory.objects.get(slug=self.kwargs['sub_slug'])
        return context

    def get_queryset(self):
        subcategory = SubCategory.objects.get(slug=self.kwargs['sub_slug'])
        return Product.objects.filter(subcategory=subcategory)

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(SubCategoryItemsListView, self).dispatch(*args, **kwargs)


@staff_member_required
def requested_products(request):
    requested_products = RequestedProduct.objects.all().order_by('-created')
    context = {
        "requested_products": requested_products,
    }
    return render(request, "backend/requested_products.html", context)


class RequestedProductDetailView(DetailView):
    model = RequestedProduct
    template_name = "backend/requested_products_detailview.html"

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(RequestedProductDetailView, self).dispatch(*args, **kwargs)


class RequestedProductUpdateView(UpdateView):
    model = RequestedProduct
    template_name = "backend/requested_products_updateview.html"
    fields = ['status', 'note']

    def get_success_url(self):
        return reverse('backend:requested-products-detail-view', args=(self.object.id,))

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(RequestedProductUpdateView, self).dispatch(*args, **kwargs)


@staff_member_required
def orders(request):
    orders = Order.objects.all().order_by('-created')
    context = {
        "orders": orders,
    }
    return render(request, "backend/orders.html", context)


def status_colour(status_id):
    if status_id == 1:
        colour = 'primary'
    elif status_id == 2:
        colour = 'info'
    elif status_id == 3:
        colour = 'success'
    elif status_id == 4:
        colour = 'danger'
    else:
        colour = 'warning'
    return colour


class OrderDetailView(DetailView):
    model = Order
    template_name = "backend/order-detail.html"

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data()
        context['items'] = OrderItem.objects.filter(order=self.object)
        context['colour'] = status_colour(self.object.status)
        return context

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(OrderDetailView, self).dispatch(*args, **kwargs)


class OrderChangeStatusUpdateView(UpdateView):
    model = Order
    fields = ['status']
    template_name = "backend/order-change-status-update-view.html"
    success_url = "../../details/"


@staff_member_required
def prescriptions(request):
    prescriptions = Prescription.objects.order_by('-created')
    context = {
        "prescriptions": prescriptions,
    }
    return render(request, "backend/prescription.html", context)


class PrescriptionDetailView(DetailView):
    model = Prescription
    template_name = "backend/prescription-detail.html"

    def get_context_data(self, **kwargs):
        context = super(PrescriptionDetailView, self).get_context_data()
        user = Prescription.objects.get(id=self.kwargs['pk']).user
        context['address'] = Address.objects.filter(user=user)
        return context


    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(PrescriptionDetailView, self).dispatch(*args, **kwargs)


@staff_member_required
def Users(request):
    users = User.objects.all()
    context = {
        "users": users,
    }
    return render(request, "backend/users.html", context)


@staff_member_required
def user_detail(request, pk):
    user = User.objects.get(id=pk)
    addresses = Address.objects.filter(user=user)
    orders = Order.objects.filter(user=user)
    return render(request, "backend/user-detail.html", { "user": user, "addresses": addresses, "orders": orders })


@staff_member_required
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

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(MiscSettingsUpdateView, self).dispatch(*args, **kwargs)
