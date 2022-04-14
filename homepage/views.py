from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import EmailForm, NewUserForm
from .tokens import account_activation_token


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

            current_site = get_current_site(request)
            mail_subject = 'Активация акканта на MyHappyPage'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            messages.success(request,
                             "Отлично! Для регистрации осталось только подтвердить"
                             " вашу почту. Мы отправили вам письмо с ссылкой.")

            return redirect("index")

        messages.error(request, form.errors)
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def activate(request, uidb64, token):
    _user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = _user.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, _user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Отлично! Вы зарегестрированы.")
        login(request, user)
        return redirect("index")
    else:
        messages.error(request, "Неправильная ссылка активации!")
        return redirect("index")


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
