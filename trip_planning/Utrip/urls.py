from django.urls import path, include
from django.contrib import admin
from .views import *




urlpatterns = [
    path('', home, name='index'),
    path('', include('estimation.urls')),
    path('', include('hotels.urls')),
    path('', include('blog.urls')),
    path('', include('trip_proposal.urls')),
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
    path('search/', search, name='search'),
    path('submit_review/<int:DetailedDesc_id>/', submit_review, name='submit_review'),
    path('faq/', faq_view,name='faq')
] 