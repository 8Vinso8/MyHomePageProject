from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from friendship.models import Friend

from .forms import EmailForm, NewUserForm, UpdateUserForm, UpdateProfileForm, NewPostForm
from .models import User, Post
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
                if next_url:
                    return redirect(next_url)
                return redirect("index")
            else:
                messages.error(request, "Неправильный логин или пароль.")
        else:
            messages.error(request, form.errors)
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "Вы успешно вышли.")
    return redirect("index")


@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    if request.user == user:
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Профиль обновлен')
                return redirect("/profile/" + user.username)
        else:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileForm(instance=request.user.profile)

        return render(request, 'own_profile.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        is_friend = Friend.objects.are_friends(request.user, user)
        friend_request = ""
        request_id = None
        if not is_friend:
            request_filter = \
                list(filter(lambda x: x.from_user_id == user.id, Friend.objects.unrejected_requests(user=request.user)))
            if request_filter:
                friend_request = "them"
                request_id = request_filter[0].id
            request_filter = \
                list(filter(lambda x: x.from_user_id == request.user.id, Friend.objects.unrejected_requests(user=user)))
            if request_filter:
                friend_request = "you"
                request_id = request_filter[0].id
        return render(request, "profile.html",
                      {"other_user": user, "friends": is_friend, "friend_request": friend_request,
                       "request_id": request_id})


@login_required
def friends(request, username):
    user = User.objects.get(username=username)
    is_self = user == request.user
    friend_list = Friend.objects.friends(user)
    them_requests = None
    you_requests = None
    if is_self:
        you_requests = Friend.objects.sent_requests(user=request.user)
        them_requests = Friend.objects.unrejected_requests(user=request.user)
    return render(request, "friends.html",
                  {"is_self": is_self, "other_user": user, "friends": friend_list, "them_requests": them_requests,
                   "you_requests": you_requests})


@login_required
def send_friendship_request(request, username):
    user = User.objects.get(username=username)
    Friend.objects.add_friend(request.user, user)
    return redirect("/profile/" + user.username)


@login_required
def cancel_friendship_request(request, username):
    user = User.objects.get(username=username)
    request_filter = \
        list(filter(lambda x: x.from_user_id == request.user.id, Friend.objects.unrejected_requests(user=user)))
    request_filter[0].cancel()
    return redirect("/profile/" + user.username)


@login_required
def reject_friendship_request(request, username):
    user = User.objects.get(username=username)
    request_filter = \
        list(filter(lambda x: x.from_user_id == user.id, Friend.objects.unrejected_requests(user=request.user)))
    request_filter[0].cancel()
    return redirect("/profile/" + user.username)


@login_required
def accept_friend(request, username):
    user = User.objects.get(username=username)
    request_filter = \
        list(filter(lambda x: x.from_user_id == user.id, Friend.objects.unrejected_requests(user=request.user)))
    request_filter[0].accept()
    return redirect("/profile/" + user.username)


@login_required
def unfriend(request, username):
    user = User.objects.get(username=username)
    Friend.objects.remove_friend(request.user, user)
    return redirect("/profile/" + user.username)


@login_required
def all_users(request):
    all_active_users = filter(lambda x: (not x.is_superuser) and x.is_active and x != request.user, User.objects.all())
    return render(request, "all_users.html", {"all_active_users": all_active_users})


@login_required
def make_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/posts/view/user/" + request.user.username)
    return render(request, "make_post.html", {"form": NewPostForm})


@login_required
def view_posts(request, mode, username=None):
    posts = None
    mode_text = None
    if mode not in ["all", "friends", "user"]:
        raise Http404
    elif mode == "user":
        user = User.objects.get(username=username)
        if user:
            posts = list(filter(lambda post: post.author == user, Post.objects.all().order_by("-date_time")))
            mode_text = "Посты " + user.username
        else:
            raise Http404
    elif mode == "all":
        posts = Post.objects.all().order_by("-date_time")
        mode_text = "Все посты"
    elif mode == "friends":
        posts = list(filter(lambda post: Friend.objects.are_friends(request.user, post.author),
                            Post.objects.all().order_by("-date_time")))
        mode_text = "Посты друзей"
    return render(request, "posts.html", {"posts": posts, "mode_text": mode_text})
