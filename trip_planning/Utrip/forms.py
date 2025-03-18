from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date


class ReviewForm1(forms.ModelForm):
    RATING_CHOICES = [
        (5, "5 Stars"),
        (4.5, "4.5 Stars"),
        (4, "4 Stars"),
        (3.5, "3.5 Stars"),
        (3, "3 Stars"),
        (2.5, "2.5 Stars"),
        (2, "2 Stars"),
        (1.5, "1.5 Stars"),
        (1, "1 Star"),
        (0.5, "0.5 Star"),
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)
    review = forms.CharField(widget=forms.Textarea(attrs={"rows": 4, "class": "form-control", "placeholder": "Write your review here..."}))

    class Meta:
        model = ReviewRating
        fields = ['rating', 'review']


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match.")


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'phone', 'email', 'profile_picture']
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class TripProposalForm(forms.ModelForm):
    date = forms.DateField(
            widget=forms.DateInput(attrs={
            'type': 'date',
            'id': 'trip-date', 
            'min': date.today().isoformat()            })
        )
    email = forms.EmailField(label="Invitee Email", required=False)
    phone_number = forms.CharField(
        max_length=20,
        help_text="Enter the recipient's phone number with country code (e.g., +1234567890).",
        required=True  
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label="City",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True 
    )
    destination = forms.ModelChoiceField(
        queryset=Destination.objects.all(),
        label="Destination",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = TripProposal
        fields = ['city', 'destination', 'date', 'email', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        destination = cleaned_data.get('destination')

        # Ensure at least one of city or destination is provided
        if not city and not destination:
            raise forms.ValidationError("Please select either a city or a destination.")

        return cleaned_data
    

    
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class EstimationForm(forms.Form):
    destination = forms.ModelChoiceField(queryset=City.objects.all())
    accommodation_type = forms.CharField(max_length=50)
    transportation_type = forms.CharField(max_length=50)
    num_nights = forms.IntegerField(min_value=1)
    num_people = forms.IntegerField(min_value=1)
