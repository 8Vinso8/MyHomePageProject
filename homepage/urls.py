from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cats/', views.cats, name='cats'),
    path('mail/', views.mail, name='mail'),
    path('registration/', views.register_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('profile/<username>', views.profile, name='profile'),
    path('activate/(<uidb64>/(<token>',
         views.activate, name='activate'),
]
urlpatterns += staticfiles_urlpatterns()
