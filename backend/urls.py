from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),

    url(r'^items/$', views.items, name='items'),
    url(r'^items/(?P<slug>.*)/details/$', views.ItemDetailView.as_view(), name='item-detail-view'),
    url(r'^items/(?P<slug>.*)/edit/$', views.ItemUpdateView.as_view(), name='item-update-view'),
    url(r'^items/create/', views.ItemCreateView.as_view(), name='item-create-view'),

    url(r'^manufacturers/$', views.manufacturers, name='manufacturers'),
    url(r'^manufacturers/create/$', views.ManufacturerCreateView.as_view(), name='manufacturer-create-view'),
    url(r'^manufacturers/(?P<slug>.*)/items/$', views.ManufacturerItemsListView.as_view(), name='manufacturer-items-list-view'),

    url(r'^categories/$', views.categories, name='categories'),
    url(r'^categories/create/$', views.CategoryCreateView.as_view(), name='category-create-view'),
    url(r'^categories/(?P<slug>.*)/items/$', views.CategoryItemsListView.as_view(), name='category-items-list-view'),
    url(r'^categories/(?P<slug>.*)/(?P<sub_slug>.*)/', views.SubCategoryItemsListView.as_view(), name='sub-category-items-list-view'),

    url(r'^requested/products/$', views.requested_products, name='requested_products'),
    url(r'^requested/products/(?P<pk>\d+)/details/$', views.RequestedProductDetailView.as_view(), name='requested-products-detail-view'),
    url(r'^requested/products/(?P<pk>\d+)/edit/$', views.RequestedProductUpdateView.as_view(), name='requested-products-update-view'),

    url(r'^orders/$', views.orders, name='orders'),
    url(r'^orders/(?P<pk>\d+)/details/$', views.OrderDetailView.as_view(), name='order-detail-view'),
    url(r'^orders/(?P<pk>\d+)/change/status/', views.OrderChangeStatusUpdateView.as_view(), name='order-change-status-update-view'),

    url(r'^prescriptions/$', views.prescriptions, name='prescriptions'),
    url(r'^prescriptions/(?P<pk>\d+)/$', views.PrescriptionDetailView.as_view(), name='prescription-detail-view'),

    url(r'^users/$', views.Users, name='users'),
    url(r'^users/(?P<pk>\d+)/$', views.user_detail, name='users-detail'),

    url(r'^misc/settings/$', views.MiscView, name='misc'),
    url(r'^misc/settings/(?P<pk>\d+)/edit/', views.MiscSettingsUpdateView.as_view(), name='misc-settings-updateview'),
]
