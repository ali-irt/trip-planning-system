from django import forms
from .models import TripProposal
from Utrip.models import City  
from django.contrib.auth.models import User

class TripProposalForm(forms.ModelForm):

    date = forms.DateField(widget=forms.SelectDateWidget(), label="Date")
    email = forms.EmailField(label="Invitee Email or WhatsApp")
    destination = forms.ModelChoiceField(
    queryset=City.objects.all(),
    label="Select City"
)

    class Meta:
        model = TripProposal
        fields = ['destination', 'date'] 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Additional customization (if needed) can go here
