from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add/to/monthly/(?P<slug>.*)/$', views.add_to_monthly, name='add-to-monthly'),
    url(r'^remove/from/monthly/(?P<slug>.*)/$', views.remove_from_monthly, name='remove-from-monthly'),
    url(r'^delete/from/monthly/(?P<slug>.*)/$', views.delete_from_monthly, name='delete-from-monthly'),

    url(r'^add/(?P<slug>.*)/$', views.add_to_cart, name='add-to-cart'),
    url(r'^remove/(?P<slug>.*)/$', views.remove_from_cart, name='remove-from-cart'),
    url(r'^delete/(?P<slug>.*)/', views.delete_from_cart, name='delete-from-cart'),

    url(r'^monthly/order/$', views.monthly_order, name='monthly-order'),

    url(r'^transfer/order/$', views.transfer_order, name='transfer-order'),
]
