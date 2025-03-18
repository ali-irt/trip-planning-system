from django.urls import path , include

from .views import *


urlpatterns = [

    path('hotel-registration/', hotel_view, name='hotel_view'),
    path('vehicle-registration/', trans, name='trans'),
    path('hotels/', hotel_list ,name='hotels'),
    path('hotel-details/<int:hotelid>', hotel_details , name= 'hotel_details'),
 ]