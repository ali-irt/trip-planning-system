from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('Utrip.urls')),
    path('admin/', admin.site.urls),
]
