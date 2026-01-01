from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Listing(models.Model):
    AMENITY_CHOICES = (
        ('wifi', 'WiFi'),
        ('pool', 'Pool'),
        ('kitchen', 'Kitchen'),
        ('ac', 'Air Conditioning'),
        ('heating', 'Heating'),
        ('washer', 'Washer'),
        ('dryer', 'Dryer'),
        ('parking', 'Parking'),
    )

    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    max_guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    bedrooms = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    bathrooms = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    amenities = models.ManyToManyField('Amenity', blank=True)
    image = models.ImageField(upload_to='listings/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.host.username}"


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name
