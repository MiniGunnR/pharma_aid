from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add/to/monthly/(?P<slug>.*)/$', views.add_to_monthly, name='add-to-monthly'),

    url(r'^add/(?P<slug>.*)/$', views.add_to_cart, name='add-to-cart'),
    url(r'^remove/(?P<slug>.*)/$', views.remove_from_cart, name='remove-from-cart'),
    url(r'^delete/(?P<slug>.*)/', views.delete_from_cart, name='delete-from-cart'),

    url(r'^monthly/order/$', views.monthly_order, name='monthly-order'),
]
