from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cats/', views.cats, name='cats'),
    path('mail/', views.mail, name='mail'),
    path('registration/', views.register_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('profile/<username>', views.profile, name='profile'),
    path('activate/(<uidb64>/(<token>', views.activate, name='activate'),
    path('friends/<username>', views.friends, name='friends'),
    path('friendship/add_friend/<username>', views.send_friendship_request, name='add_friend'),
    path('friendship/cancel/<username>', views.cancel_friendship_request, name='cancel_fr_request'),
    path('friendship/reject/<username>', views.reject_friendship_request, name='reject_fr_request'),
    path('friendship/accept/<username>', views.accept_friend, name='accept_friend'),
    path('friendship/unfriend/<username>', views.unfriend, name='unfriend'),
    path('users/all', views.all_users, name='all_users'),
    path('posts/view/<mode>', views.view_posts, name='view_user_posts'),
    path('posts/view/<mode>/<username>', views.view_posts, name='view_user_posts'),
    path('posts/makePost', views.make_post, name='make_post'),
]
urlpatterns += staticfiles_urlpatterns()
