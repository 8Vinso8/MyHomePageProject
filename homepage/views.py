from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render

from .forms import EmailForm


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
            subject = "Письмо счастья"
            message = \
                """Это письмо обошло вокруг света восемнадцать раз! Если вы перепишете его семь раз, следующие семь 
                лет вам будет во всем везти, а через 12 часов с вами произойдет что-то очень хорошее! А если вы его 
                не перепишете, то вас ждет семь лет несчастий! Вы думаете, это неправда. А это правда! Одна девочка 
                переписала это письма, и на следующий день к ней посватался богатый жених! А один человек не стал 
                переписывать, потому что не умел писать, и его высадили с корабля прямо на необитаемый остров, 
                а потом крокодил откусил ему руку! Нельзя, чтобы цепь писем оборвалась! """
            from_email = "happymail@gmail.com"
            try:
                send_mail(subject, message, from_email, [email])
            except BadHeaderError:
                return HttpResponse('Invalid Header found')
            return render(request, "sent.html", {})
    return render(request, "mail.html", {'form': form})


def register(request):
    return render("register.html")


def login(request):
    return render("login.html")
