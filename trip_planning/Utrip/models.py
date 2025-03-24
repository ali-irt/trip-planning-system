from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.core.validators import MinValueValidator
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


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
    featured_img = models.ImageField(upload_to='pictures/pics')
    img1 = models.ImageField(upload_to='pictures/pics')
    img2 = models.ImageField(upload_to='pictures/pics')
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    city = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  # International formats
    email = models.EmailField(max_length=254)
    profile_picture = models.ImageField(upload_to='pictures/profile_pictures/', default='profile_pictures/default.jpg', blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('declined', 'Declined'),
    ('completed', 'Completed'),
]

class TripProposal(models.Model):

    proposer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals')
    destination = models.ManyToManyField(Destination, related_name='trip_proposals')
    date = models.DateField()
    invitees = models.ManyToManyField(User, related_name='trip_invites')  # Invitees
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Trip by {self.proposer} on {self.date}"



class Type(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    def __str__(self):
        return self.type



class Accommodation(models.Model):
    owner = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    destination = models.ForeignKey('City', on_delete=models.CASCADE)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    contact = models.CharField(max_length=20)
    img1 = models.ImageField(upload_to='pictures/pics_rooms/', blank=True, null=True)
    img2 = models.ImageField(upload_to='pictures/pics_rooms/', blank=True, null=True)
    address = models.TextField()
    business_license = models.FileField(upload_to='documents/business_licenses/')
    registration_certificate = models.FileField(upload_to='documents/registration_certificates/')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name) if self.name else "Unnamed"



class Transportation(models.Model):
    Vtype=[
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('offroader', 'Offroader'),
        ('hatchback', 'Hatchback'),
        ('crossover', 'Crossover'),
        ('hybrid', 'Hybrid'),
    ]
    origin = models.ForeignKey(City, on_delete=models.CASCADE)
    type = models.CharField(max_length=50,choices=Vtype,default='sedan')
    registeration_number = models.CharField(max_length=20)
    average_rent = models.DecimalField(max_digits=10, decimal_places=2)
    img1 = models.ImageField(upload_to='pictures/pics_vehicle', blank=True, null=True)
    img2 = models.ImageField(upload_to='pictures/pics_vehicle', blank=True, null=True)


    def __str__(self):
        return self.registeration_number
# def __str__ function is used to return exact name as entered otherwise it will return 'destination obect'



class Blog(models.Model):
    title = models.CharField(null=False, max_length=100)
    blog = models.CharField(null=False, max_length=1000)
    img1 = models.ImageField(upload_to='pictures/pics_blog')
    img2 = models.ImageField(upload_to='pictures/pics_blog')
    published_date = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=200, blank=True)
    featured_image = models.ImageField(upload_to='pictures/pics_blog', blank=True, null=True)

    def __str__(self):
        return self.title
class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    def average_review(self):
        reviews = Reviews.objects.filter(blog=self, status=True).aggregate(average=Avg('rating'))
        return float(reviews['average']) if reviews['average'] is not None else 0

    def count_review(self):
        reviews = Reviews.objects.filter(blog=self, status=True).aggregate(count=Count('id'))
        return int(reviews['count']) if reviews['count'] is not None else 0
