from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from .forms import EmailForm
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


def index(request):
    return render(request, 'index.html', {})


def cats(request):
    return render(request, 'cats.html', {})


def mail(request):
    if request.method == 'GET':
        form = EmailForm()
    else:
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = "Радостное письмо!"
            message = "Желаем вам радости и светлого будущего!"
            from_email = "happymail@gmail.com"
            try:
                send_mail(subject, message, from_email, [email])
            except BadHeaderError:
                return HttpResponse('Invalid Header found')
            return redirect('sent')
    return render(request, "mail.html", {'form': form})


def sent(request):
    return render(request, 'sent.html', {})
