from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['booking__listing__title', 'booking__guest__username']
