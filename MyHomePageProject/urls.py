# MyHomePageProject URL Configuration


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
]

handler404 = 'MyHomePageProject.views.page_not_found_view'
