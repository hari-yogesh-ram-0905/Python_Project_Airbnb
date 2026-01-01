from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    def get_hashed_password(self):
        """Return the stored hashed password string.

        This is the hashed value stored in the database (e.g. "pbkdf2_sha256$...").
        Use this only for debugging or test verification — do NOT expose in production APIs.
        """
        return self.password

    def verify_password(self, raw_password):
        """Return True if `raw_password` matches the user's password."""
        return self.check_password(raw_password)

    def __str__(self):
        return f"{self.username} ({self.role})"