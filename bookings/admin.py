from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['guest', 'listing', 'check_in_date', 'check_out_date', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['guest__username', 'listing__title']
