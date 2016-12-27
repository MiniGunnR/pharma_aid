from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^our/story/$', views.our_story, name='our_story'),
    url(r'^store/$', views.store, name='store'),
    url(r'^contact/us/$', views.contact_us, name='contact_us'),
    url(r'^terms/of/use/$', views.terms_of_use, name='terms_of_use'),

    url(r'^send/mail/$', views.send_anon_mail, name='send_anon_mail'),
]
