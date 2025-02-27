from django import forms
from estimation.models import  Accommodation, Transportation

class hotelform(forms.ModelForm):
    class Meta:
        model = Accommodation

        fields = '__all__'
class TransportationForm(forms.ModelForm):
    class Meta:
        model = Transportation
        fields = '__all__'