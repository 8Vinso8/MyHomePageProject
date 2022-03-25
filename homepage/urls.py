from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='index'),
    path('cats/', views.cats, name='cats'),
    path('mail/', views.mail, name='mail'),
    path('sent/', views.sent, name='sent'),
]
urlpatterns += staticfiles_urlpatterns()
