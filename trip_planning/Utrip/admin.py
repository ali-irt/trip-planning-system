from django.contrib import admin
from .models import *

class DestinationAdmin(admin.ModelAdmin):
    fields = ('city', 'destination_spot', 'keywords', 'category', 'featured_img', 'img1', 'img2', 'description')

    list_display = ('destination_spot', 'city', 'category', 'keywords', 'featured_img')

    search_fields = ('destination_spot', 'city__name', 'keywords')

    list_filter = ('category', 'city')

admin.site.register(City)
admin.site.register(Category)
admin.site.register(Faq)
admin.site.register(ReviewRating)
admin.site.register(Destination, DestinationAdmin)
