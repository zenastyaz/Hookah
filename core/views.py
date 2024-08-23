from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def delivery(request):
    return render(request, 'delivery.html')


def terms(request):
    return render(request, 'terms.html')
