from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.core.validators import MinValueValidator
import random

class City(models.Model):
    PAKISTAN_PROVINCES = [
        ('Punjab', 'Punjab'),
        ('Sindh', 'Sindh'),
        ('Khyber Pakhtunkhwa', 'Khyber Pakhtunkhwa'),
        ('Balochistan', 'Balochistan'),
        ('Islamabad Capital Territory', 'Islamabad Capital Territory'),
        ('Azad Jammu & Kashmir', 'Azad Jammu & Kashmir'),
        ('Gilgit-Baltistan', 'Gilgit-Baltistan'),
    ]
    
    name = models.CharField(max_length=50)
    province = models.CharField(max_length=30, choices=PAKISTAN_PROVINCES)
    def __str__(self):
        return self.name
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    def __str__(self):
        return self.category_name

class Destination(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    destination_spot = models.CharField(max_length=100, null=True)
    keywords = models.CharField(max_length=250)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    featured_img = models.ImageField(upload_to='pics')
    img1 = models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    description = models.TextField()
    def __str__(self):
        return self.destination_spot

class Faq(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    def __str__(self):
        return self.question



class ReviewRating(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(blank=True)
    rating = models.FloatField(validators=[MinValueValidator(1.0)])  # Ensure a minimum rating
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    @property
    def average_review(self):
        reviews = self.destination.reviews.filter(status=True).aggregate(average=Avg('rating'))
        return float(reviews['average']) if reviews['average'] is not None else 0

    @property
    def count_review(self):
        reviews = self.destination.reviews.filter(status=True).aggregate(count=Count('id'))
        return int(reviews['count']) if reviews['count'] is not None else 0


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.otp}"

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    city = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Allow more digits for international formats
    email = models.CharField(max_length=15, blank=True, null=True)  
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg', blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username