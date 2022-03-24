from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'index.html', {})


def cats(request):
    return render(request, 'cats.html', {})


def mail(request):
    return render(request, 'mail.html', {})