import random, os, string, math, datetime, calendar

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.db import transaction
from django.core.urlresolvers import reverse_lazy

from django.views.generic.edit import CreateView

from act.models import Address
from .models import Order, OrderItem, RequestedProduct, Prescription
from cart.models import Cart, CartItem
from utils.models import Misc

from .forms import RequestProductForm, PrescriptionForm


def address_check(user):
    return Address.objects.filter(user=user).exists()

def cart_not_empty(user):
    try:
        Cart.objects.get(owner=user)
    except Cart.DoesNotExist:
        return False
    else:
        return Cart.objects.get(owner=user).items != 0

def user_has_mobile(user):
    return user.mobile != ''


@login_required
@user_passes_test(address_check, login_url='/my_account/add/address/')
@user_passes_test(user_has_mobile, login_url='/my_account/add/mobile/')
@user_passes_test(cart_not_empty, login_url='/')
def PlaceOrder(request):
    my_addresses = Address.objects.filter(user=request.user)
    default_address = Address.objects.get(user=request.user, default=True)

    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    day_after_tomorrow = datetime.date.today() + datetime.timedelta(days=2)

    delivery_dates = (
        (today, 'Today'),
        (tomorrow, 'Tomorrow'),
        (day_after_tomorrow, '{0} {1} {2}'.format(day_after_tomorrow.day, calendar.month_abbr[day_after_tomorrow.month], day_after_tomorrow.year))
    )

    delivery_times = Order.DELIVERY_TIMES
    return render(request, "order/place-order.html", locals())


def GetAddress(request, pk):
    address = Address.objects.get(id=pk)
    details = address.addressinfo
    return JsonResponse({"name": details.name,
                         "address_1": details.address_1,
                         "address_2": details.address_2,
                         "city": details.city,
                         "zip": details.zip,
                         "country": details.country})

@login_required
@transaction.atomic
def ConfirmOrder(request):
    items = request.POST

    request.session['address'] = int(items['address_options'])
    address = Address.objects.get(id=request.session['address'])
    details = address.addressinfo

    request.session['delivery_date'] = items['delivery_date']
    date = request.session['delivery_date']

    request.session['delivery_time'] = Order.DELIVERY_TIMES[int(items['delivery_time']) - 1]
    time = request.session['delivery_time'][1]

    request.session['payment'] = int(items['payment_options'])
    payment = Order.PAYMENT_METHODS[request.session['payment'] - 1][1]

    context = {
        "address": address,
        "details": details,
        "date": date,
        "time": time,
        "payment": payment}

    if items['payment_options'] == "2":
        context["trx"] = True

    cart = Cart.objects.get(owner=request.user)

    dc_obj = Misc.objects.get(item='delivery_charge')
    min_obj = Misc.objects.get(item='min_order_for_free_delivery')
    if cart.total < min_obj.value:
        delivery_charge = dc_obj.value
    else:
        delivery_charge = 0
    request.session['delivery_charge'] = delivery_charge

    total = math.ceil((cart.total) + delivery_charge)
    request.session['total'] = total

    context.update({"subtotal": cart.total, "delivery_charge": delivery_charge, "total": total})

    return render(request, "order/confirm-order.html", context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def SaveOrder(request):
    if request.method == "POST":
        status = Order.SUBMITTED
        ip_address = get_client_ip(request)
        user = request.user
        # transaction_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        transaction_id = ''.join(random.choice(string.digits) for _ in range(10))
        email = user.email
        mobile = user.mobile

        address = Address.objects.get(id=int(request.POST['address']))

        shipping_name = address.addressinfo.name
        shipping_address_1 = address.addressinfo.address_1
        shipping_address_2 = address.addressinfo.address_2
        shipping_city = address.addressinfo.city
        shipping_zip = address.addressinfo.zip
        shipping_country = address.addressinfo.country

        billing_name = address.addressinfo.name
        billing_address_1 = address.addressinfo.address_1
        billing_address_2 = address.addressinfo.address_2
        billing_city = address.addressinfo.city
        billing_zip = address.addressinfo.zip
        billing_country = address.addressinfo.country

        delivery_date = request.POST['date']
        delivery_time = int(request.POST['time'])

        payment_method = int(request.POST['payment'])
        if 'trx_id' in request.POST:
            trx_id = request.POST['trx_id']
        else:
            trx_id = ''

        delivery_charge = int(request.POST['delivery_charge'])

        order = Order.objects.create(status=status,
                                     ip_address=ip_address,
                                     user=user,
                                     transaction_id=transaction_id,
                                     email=email,
                                     mobile=mobile,
                                     shipping_name=shipping_name,
                                     shipping_address_1=shipping_address_1,
                                     shipping_address_2=shipping_address_2,
                                     shipping_city=shipping_city,
                                     shipping_zip=shipping_zip,
                                     shipping_country=shipping_country,
                                     billing_name=billing_name,
                                     billing_address_1=billing_address_1,
                                     billing_address_2=billing_address_2,
                                     billing_city=billing_city,
                                     billing_zip=billing_zip,
                                     billing_country=billing_country,
                                     delivery_date=delivery_date,
                                     delivery_time=delivery_time,
                                     payment_method=payment_method,
                                     trx_id=trx_id,
                                     delivery_charge=delivery_charge)

        cart = Cart.objects.get(owner=request.user)
        cartitems = CartItem.objects.filter(cart=cart)
        for item in cartitems:
            OrderItem.objects.create(order=order,
                                 product=item.product,
                                 quantity=item.quantity,
                                 price=item.price())
            item.delete()
        cart.total = 0
        cart.items = 0
        cart.save()
        return HttpResponseRedirect('/')
    else:
        return


def PastOrders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, "order/past-orders.html", {"orders": orders})


def OrderDetails(request, transaction_id):
    order = Order.objects.get(transaction_id=transaction_id)
    orderitems = OrderItem.objects.filter(order=order)
    return render(request, "order/order-details.html", {"order": order, "orderitems": orderitems})


def RequestProduct(request):
    objs = RequestedProduct.objects.filter(user=request.user)
    if request.method == "POST":
        form = RequestProductForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            os.system('echo "A new request has been placed for a product by %s" | mail -s "Product Requested by a User" hasan.mohaiminul@gmail.com' % f.user.get_full_name())
            return HttpResponseRedirect('/order/request/a/product/')
    else:
        form = RequestProductForm()
    return render(request, "order/request-product.html", {"form": form, "requested_products": objs})

from django.utils.decorators import method_decorator
class UploadPrescription(CreateView):
    model = Prescription
    fields = ['image']
    template_name = 'order/upload-prescription.html'
    success_url = reverse_lazy('order:upload-prescription')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(UploadPrescription, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UploadPrescription, self).get_context_data()
        context['prescriptions'] = Prescription.objects.filter(user=self.request.user)
        return context

    @method_decorator(user_passes_test(address_check, login_url='/my_account/add/address/'))
    @method_decorator(user_passes_test(user_has_mobile, login_url='/my_account/add/mobile/'))
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)
