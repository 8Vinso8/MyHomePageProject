from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cats/', views.cats, name='cats'),
    path('mail/', views.mail, name='mail'),
    path('registration/', views.register, name='registration'),
    path('login/', views.login, name='login'),
]
urlpatterns += staticfiles_urlpatterns()
