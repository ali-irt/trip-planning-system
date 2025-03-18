from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count

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
