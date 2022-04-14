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
    path('profile/', views.profile, name='profile'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         views.activate, name='activate'),
]
urlpatterns += staticfiles_urlpatterns()
