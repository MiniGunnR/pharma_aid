from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^my/addresses/$', views.MyAddresses, name='my-addresses'),
    url(r'^add/address/$', views.AddAddress, name='add-address'),
    url(r'^make/address/(?P<pk>\d+)/default/$', views.MakeAddressDefault, name='make-address-default'),
    url(r'^add/mobile/$', views.AddMobile, name='add-mobile'),
    url(r'^profile/$', views.Profile, name='profile'),
]
