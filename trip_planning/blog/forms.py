from django import forms
from .models import Reviews

class ReviewForm(forms.ModelForm):
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
        model = Reviews
        fields = ['rating', 'review']