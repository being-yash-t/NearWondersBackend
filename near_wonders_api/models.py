from django.db import models
from django.contrib.auth.models import User


class Season(models.TextChoices):
    SUMMER = 'summer', 'Summer'
    WINTER = 'winter', 'Winter'
    SPRING = 'spring', 'Spring'
    AUTUMN = 'autumn', 'Autumn'


class Activity(models.TextChoices):
    TREK = 'trek', 'Trek'
    CAMP = 'camp', 'Camp'
    BIKE_TRAIL = 'bike-trail', 'Bike Trail'
    OFF_ROAD_TRAIL = 'off-road-trail', 'Off Road Trail'


class Location(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    activities = models.CharField(
        max_length=255,
        choices=Activity.choices,
        blank=True,
        null=True
    )
    best_season = models.CharField(
        max_length=255,
        choices=Season.choices,
        blank=True,
        null=True
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_by = models.ForeignKey(User, related_name='locations', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def preview_images(self):
        return self.images.all()[:4]


class Image(models.Model):
    location = models.ForeignKey(Location, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='location_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.location.name}"


class UserActivity(models.Model):
    user = models.ForeignKey(User, related_name='activities', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, related_name='user_activities', on_delete=models.CASCADE)
    activities = models.CharField(max_length=255, choices=Activity.choices)
    user_notes = models.TextField(blank=True, null=True)
    images = models.ManyToManyField(Image, related_name='user_activities')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Activity by {self.user.username} at {self.location.name}"
