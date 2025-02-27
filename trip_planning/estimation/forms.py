from django import forms
from Utrip.models import *

class EstimationForm(forms.Form):
    destination = forms.ModelChoiceField(queryset=City.objects.all())
    accommodation_type = forms.CharField(max_length=50)
    transportation_type = forms.CharField(max_length=50)
    num_nights = forms.IntegerField(min_value=1)
    num_people = forms.IntegerField(min_value=1)
