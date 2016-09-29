from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get/address/(?P<pk>\d+)/$', views.GetAddress, name='get-address'),
    url(r'^place/order/$', views.PlaceOrder, name='place-order'),
    url(r'^confirm/order/$', views.ConfirmOrder, name='confirm-order'),
    url(r'^save/order/$', views.SaveOrder, name='save-order'),

    url(r'^past/orders/$', views.PastOrders, name='past-orders'),
    url(r'^past/orders/(?P<transaction_id>.*)/$', views.OrderDetails, name='order-details'),

    url(r'^request/a/product/$', views.RequestProduct, name='request-product'),

    url(r'^upload/prescription/$', views.UploadPrescription.as_view(), name='upload-prescription'),
]


