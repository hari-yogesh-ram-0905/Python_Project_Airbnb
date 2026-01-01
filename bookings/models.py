from django.db import models
from django.contrib.auth import get_user_model
from listings.models import Listing
from django.core.exceptions import ValidationError

User = get_user_model()


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_as_guest')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.guest.username} - {self.listing.title} ({self.check_in_date})"

    def clean(self):
        if self.check_in_date >= self.check_out_date:
            raise ValidationError("Check-out date must be after check-in date")
        
        if self.number_of_guests > self.listing.max_guests:
            raise ValidationError(f"Number of guests cannot exceed {self.listing.max_guests}")

        # Check for date conflicts
        conflicting_bookings = Booking.objects.filter(
            listing=self.listing,
            status__in=['confirmed', 'pending']
        ).exclude(id=self.id)

        for booking in conflicting_bookings:
            if not (self.check_out_date <= booking.check_in_date or self.check_in_date >= booking.check_out_date):
                raise ValidationError("Dates conflict with existing booking")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
