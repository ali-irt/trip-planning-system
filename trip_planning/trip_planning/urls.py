from django.urls import path , include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', include('Utrip.urls')),
    path('', include('hotels.urls')),
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)