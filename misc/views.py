from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import os
from django.conf import settings


def faq(request):
    page_title = "FAQ"
    return render(request, "misc/faq.html", { "page_title": page_title })


def our_story(request):
    page_title = "Our Story"
    return render(request, "misc/our_story.html", { "page_title": page_title })


def store(request):
    page_title = "Store"
    return render(request, "misc/store.html", { "page_title": page_title })


def contact_us(request):
    page_title = "Contact Us"
    if request.user.is_authenticated():
        name = request.user.get_full_name()
        phone = request.user.mobile
        email = request.user.email
    else:
        name = ''
        phone = ''
        email = ''
    return render(request, "misc/contact_us.html", { "page_title": page_title,
                                                     "name": name,
                                                     "phone": phone,
                                                     "email": email
                                                     })


def send_anon_mail(request):
    if request.method == "POST":
        file = os.path.join(settings.BASE_DIR, 'misc/mail/', 'mail.txt')
        with open (file, 'w') as f:
            f.write('From - ' + str(request.POST.get('name')))
            f.write('\n')
            f.write('Email - ' + str(request.POST.get('email')))
            f.write('\n')
            f.write('Phone - ' + request.POST.get('phone'))
            f.write('\n')
            f.write('= = = = = = = = = =\n')
            msg = str(request.POST.get('message', '')).replace('\015', '\n')
            f.write(msg)
            f.close()
        os.system('mail -s "Email from a Customer" pharmaaidltd@gmail.com < %s' % file)
        return HttpResponseRedirect('/misc/contact/us/')


def terms_of_use(request):
    page_title = "Terms of Use"
    return render(request, "misc/terms_of_use.html", { "page_title": page_title })
