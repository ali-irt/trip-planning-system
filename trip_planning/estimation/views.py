from .forms import EstimationForm
from .models import *
from django.shortcuts import render

def estimate_price(request):
    if request.method == 'POST':
        form = EstimationForm(request.POST)
        if form.is_valid():
            # Retrieve form data
            destination = form.cleaned_data['destination']
            accommodation_type = form.cleaned_data['accommodation_type']
            transportation_type = form.cleaned_data['transportation_type']
            num_nights = form.cleaned_data['num_nights']
            num_people = form.cleaned_data['num_people']

            # Calculate accommodation cost
            accommodation = Accommodation.objects.filter(destination=destination, type=accommodation_type).first()
            accommodation_cost = accommodation.average_price * num_nights * num_people if accommodation else 0

            # Calculate transportation cost
            transportation = Transportation.objects.filter(destination=destination, type=transportation_type).first()
            transportation_cost = transportation.average_price if transportation else 0

            # Calculate total price
            total_price = accommodation_cost + transportation_cost

            return render(request, 'result.html', {'total_price': total_price})
    else:
        form = EstimationForm()
    return render(request, 'estimate.html', {'form': form})
