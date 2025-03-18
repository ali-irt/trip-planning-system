from django import forms
from Utrip.models import  Accommodation, Transportation

class hotelform(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = [
            'owner',
            'name',
            'destination',
            'type',
            'average_price',
            'rooms',
            'contact',
            'address',
            'img1',
            'img2',
            'business_license',
            'registration_certificate',
        ]
class TransportationForm(forms.ModelForm):
    class Meta:
        model = Transportation
        fields = '__all__'