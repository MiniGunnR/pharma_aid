from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Address, AddressInfo, User

from .forms import AddressForm, AddressInfoForm, AddMobileForm


def MyAddresses(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, "act/my-addresses.html", locals())


def AddAddress(request):
    next_page = request.GET.get('next', '/my_account/add/address/')
    if request.method == "POST":
        form1 = AddressForm(request.POST, instance=Address())
        form2 = AddressInfoForm(request.POST, instance=AddressInfo())
        if form1.is_valid() and form2.is_valid():
            f1 = form1.save(commit=False)
            f1.user = request.user
            f1.save()
            f2 = form2.save(commit=False)
            f2.address = f1
            f2.save()
            return HttpResponseRedirect(next_page)
    else:
        form1 = AddressForm()
        form2 = AddressInfoForm()
    return render(request, "act/add-address.html", {"form1": form1, "form2": form2, "next": next_page})


def MakeAddressDefault(request, pk):
    this_address = Address.objects.get(id=pk)
    user = this_address.user

    old_address = Address.objects.get(user=user, default=True)
    old_address.default = False
    old_address.save()

    this_address.default = True
    this_address.save()
    return JsonResponse({"old_id": old_address.id, "new_id": this_address.id})


@login_required
def AddMobile(request):
    next = request.GET.get('next', '/')
    if request.method == "POST":
        form = AddMobileForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.mobile = form.cleaned_data['mobile']
            user.save()
            return HttpResponseRedirect(next)
    else:
        form = AddMobileForm()
    return render(request, "act/add-mobile.html", {"form": form, "next": next})


def Profile(request):
    return render(request, "act/profile.html")
