from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import EmailForm, NewUserForm


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


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы зарегестрированы.")
            return redirect("index")
        messages.error(request, form.errors)
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next')
                print(next_url)
                if next_url:
                    return redirect(next_url)
                return redirect("index")
            else:
                messages.error(request, "Неправильный логин или пароль.")
        else:
            messages.error(request, form.errors)
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Вы успешно вышли.")
    return redirect("index")


@login_required
def profile(request):
    return render(request, "profile.html", {})
