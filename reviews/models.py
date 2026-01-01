from django.db import models
from django.contrib.auth import get_user_model
from listings.models import Listing
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Review(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('guest', 'listing')

    def __str__(self):
        return f"Review by {self.guest.username} for {self.listing.title}"
