from django.db import models
from django.urls import reverse
from django.db.models import Avg, Count
 
 
 
class Hotel(models.Model):
    hostel_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=50, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/hostel')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
 
    def get_url(self):
        return reverse('hostel_details', args=[self.slug])
 
    def __str__(self):
        return self.hostel_name
 
    def averageReview(self):
        reviews = Review.objects.filter(hostel=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
 
    def countReview(self):
        reviews = Review.objects.filter(hostel=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
 
class Review(models.Model):
    user = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='user_reviews')
    hostel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hostel_reviews', null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    review = models.TextField(max_length=250, null=True, blank=True)
    ip = models.CharField(max_length=50, blank=True)
    rating = models.IntegerField(default=1)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.id)

