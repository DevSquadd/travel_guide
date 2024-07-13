from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models as geomodels


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_place = models.CharField(max_length=255)
    bio = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    reset_password_token = models.CharField(max_length=100, blank=True)
    new_email = models.EmailField(blank=True)
    current_location = models.PointField(blank=True, null=True)  # GeoDjango field for location detection

    def __str__(self):
        return self.user.username

from django.contrib.gis.db import models as geomodels

class Destination(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    latitude = geomodels.FloatField()
    longitude = geomodels.FloatField()
    high_budget_places = models.TextField()
    medium_budget_places = models.TextField()
    low_budget_places = models.TextField()
    local_attractions = models.TextField()
    local_cuisine = models.TextField()
    feedback = models.ManyToManyField(UserProfile, through='Feedback')

    def __str__(self):
        return self.name

class TravelMedium(models.Model):
    name = models.CharField(max_length=50)
    cost_per_km = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User

class TripPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    travel_medium = models.ForeignKey(TravelMedium, on_delete=models.CASCADE)
    budget = models.CharField(max_length=6, choices=(('high', 'High'), ('medium', 'Medium'), ('low', 'Low')))
    days = models.IntegerField()
    transport = models.CharField(max_length=10, choices=(('bus', 'Bus'), ('train', 'Train'), ('flight', 'Flight')))
    total_price = models.FloatField()
    roadmap = models.TextField(blank=True)
    itinerary = models.TextField(blank=True)  # Field for customizable itinerary
    pdf_guide = models.FileField(upload_to='pdf_guides/', blank=True)  # Field for offline access to trip info

    def __str__(self):
        return f"{self.user.username}'s Trip to {self.destination}"

    def calculate_budget(self):
        # Implement logic to calculate budget based on days, transport, total_price, etc.
        if self.days <= 3:
            self.budget = 'low'
        elif 4 <= self.days <= 7:
            self.budget = 'medium'
        else:
            self.budget = 'high'

    def generate_roadmap(self):
        # Implement logic to generate roadmap based on destination, transport, days, etc.
        self.roadmap = f"Roadmap for {self.destination} via {self.transport} over {self.days} days."

    def create_pdf_guide(self):
        # Implement logic to create a PDF guide for offline access
        pass

    def save(self, *args, **kwargs):
        # Calculate budget, generate roadmap, and create PDF guide before saving the instance
        self.calculate_budget()
        self.generate_roadmap()
        self.create_pdf_guide()
        super().save(*args, **kwargs)

class Feedback(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f"{self.user_profile.user.username}'s feedback on {self.destination.name}"
