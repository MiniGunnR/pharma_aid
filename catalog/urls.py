from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),

    url(r'^category/(?P<category_slug>.*)/(?P<subcategory_slug>.*)/$', views.show_subcategory, name='show_subcategory'),
    url(r'^category/(?P<category_slug>.*)/$', views.show_category, name='category'),

    url(r'^more/items/(?P<category_slug>.*)/$', views.more_items, name='more_items'),

    url(r'^product/(?P<product_slug>.*)/$', views.show_product, name='product'),

    url(r'^search/$', views.search_products, name='search-products'),

    url(r'^auto/$', views.auto, name='auto'),
]
