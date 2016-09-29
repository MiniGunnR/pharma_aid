from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^category/(?P<category_slug>.*)/$', views.show_category, name='category'),
    url(r'^product/(?P<product_slug>.*)/$', views.show_product, name='product'),

    url(r'^search/$', views.search_products, name='search-products'),

    url(r'^auto/$', views.auto, name='auto'),
]
