from django.shortcuts import render


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
    return render(request, "misc/contact_us.html", { "page_title": page_title })


def terms_of_use(request):
    page_title = "Terms of Use"
    return render(request, "misc/terms_of_use.html", { "page_title": page_title })
