from django.urls import path, include
from django.contrib import admin
from .views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', home, name='index'),
    path('about/', about, name='about'),

    path('login/', login_view, name='login'),
    path("accounts/",include("allauth.urls")),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('email-verification/', email_verification_view, name='email_verification'),
    path('verify-otp/<int:user_id>/', verify_otp_view, name='verify_otp'),

  # If destination_spot is provided, it will be captured
    path('destination_list/<str:destination_spot>/', destination_list, name='destination_list'),

    # If destination_spot is not provided, this pattern will match (with an empty string or None as destination_spot)
    path('destination_list/', destination_list, name='destination_list'),

    path('destination_details/<str:destination_name>/', destination_details, name='destination_details'),

    path('profile/',profile_user,name='profile_user'),
    path('edit_profile/',edit_profile,name='edit_profile'),
    path('search/', search, name='search'),
    path('submit_review/<int:DetailedDesc_id>/', submit_review, name='submit_review'),
    path('faq/', faq_view,name='faq'),
    path('propose-trip/', trip_proposal_view, name='propose_trip'),
    path('proposal-success/', proposal_success_view, name='proposal_success'),
    path('contact/', contact, name='contact'),
    path('estimate/', estimate_price, name='estimation'),

    path('hotel-registration/', hotel_view, name='hotel_view'),
    path('vehicle-registration/', trans, name='trans'),
    path('hotels/', hotel_list ,name='hotels'),
    path('hotel-details/<int:hotelid>', hotel_details , name= 'hotel_details'),
    path('blog/', blog, name='blog'),
    path('blog/<int:id>/',blog, name='blog'),
    path('blog_detail/', blog_detail, name='blog_detail'),
    path('blog_detail/<int:id>',blog_detail, name='blog_detail'),
    path('blog_review/<int:id>/', submit_review_blog, name='blog_review'),

]
