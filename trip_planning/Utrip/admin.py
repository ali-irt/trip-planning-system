from django.contrib import admin
from .models import *


admin.site.site_header = "WanderWise Admin"         # Top left corner title
admin.site.site_title = "WanderWise Admin Portal"   # Browser tab title
admin.site.index_title = "Welcome to WanderWise Admin"   # Dashboard welcome title



class DestinationAdmin(admin.ModelAdmin):
    fields = ('city', 'destination_spot', 'keywords', 'category', 'featured_img', 'img1', 'img2', 'description')

    list_display = ('destination_spot', 'city', 'category', 'keywords', 'featured_img')

    search_fields = ('destination_spot', 'city__name', 'keywords')

    list_filter = ('category', 'city')


class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'is_approved']
    list_filter = ['is_approved']
    actions = ['approve_hotels']

    def approve_hotels(self, request, queryset):
        queryset.update(is_approved=True)
    approve_hotels.short_description = "Approve selected hotels"

admin.site.register(Accommodation, HotelAdmin)



admin.site.register(City)
admin.site.register(Category)
admin.site.register(Faq)
admin.site.register(ReviewRating)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Type)
admin.site.register(Transportation)
admin.site.register(Blog)
admin.site.register(Reviews)