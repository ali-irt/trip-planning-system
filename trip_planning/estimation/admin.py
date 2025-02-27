from django.contrib import admin
from .models import  *

# Register your models with the admin interface
admin.site.register(Type)
admin.site.register(Accommodation)
admin.site.register(Transportation)
