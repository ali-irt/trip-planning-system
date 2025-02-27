from django.urls import path
from .views import *


urlpatterns = [

    path('propose-trip/', trip_proposal_view, name='propose_trip'),
    path('proposal-success/', proposal_success_view, name='proposal_success'),


]