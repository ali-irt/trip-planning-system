from django.shortcuts import render, redirect, get_object_or_404
from .forms import hotelform, TransportationForm
from Utrip.models import Accommodation  # Import relevant models
from django.contrib import messages  
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import hotelform  


@login_required
def hotel_view(request):
    if request.method == 'POST':
        form = hotelform(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.save()
            messages.success(request, 'Hotel details saved successfully!')
            return redirect('hotels')
        else:
            messages.error(request, 'There was an error saving the hotel details. Please check the form.')
    else:
        form = hotelform()
        
    return render(request, 'hotels.html', {'form': form})
 
def trans(request):
    if request.method == 'POST':
        form = TransportationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, 'Transportation details saved successfully!')
            return redirect('trans')  # Redirect to a success page or any other view
        else:
            messages.error(request, 'There was an error saving the transportation details.')
    else:
        form = TransportationForm()

    return render(request, 'vehicle.html', {'form': form})

def hotel_list(request):
    hotels = Accommodation.objects.filter(is_approved=True)
    context = {
        'hotels': hotels
    }
    return render(request, 'hotel_list.html', context=context)

   
def hotel_details(request, hotelid):
    hotel = get_object_or_404(Accommodation,id=hotelid)
    context = {
        'hotel': hotel
        }
    return render(request, 'hotel_details.html', context=context)