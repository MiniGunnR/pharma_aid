from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^super/', admin.site.urls),

    url(r'^backend/', include('backend.urls', namespace='backend')),

    url(r'^', include('catalog.urls', namespace='catalog')),

    url(r'^cart/', include('cart.urls', namespace='cart')),

    url(r'^order/', include('order.urls', namespace='order')),

    url(r'^my_account/', include('act.urls', namespace='my_account')),

    url(r'^pages/', include('django.contrib.flatpages.urls')),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^misc/', include('misc.urls', namespace='misc')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
