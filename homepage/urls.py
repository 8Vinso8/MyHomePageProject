from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cats/', views.cats, name='cats'),
    path('mail/', views.mail, name='mail'),
]
urlpatterns += staticfiles_urlpatterns()
