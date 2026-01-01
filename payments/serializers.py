from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source='booking.id', read_only=True)
    listing_title = serializers.CharField(source='booking.listing.title', read_only=True)
    guest_username = serializers.CharField(source='booking.guest.username', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'booking',
            'booking_id',
            'listing_title',
            'guest_username',
            'amount',
            'status',
            'stripe_payment_intent',
            'transaction_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'booking_id',
            'listing_title',
            'guest_username',
            'stripe_payment_intent',
            'transaction_id',
            'created_at',
            'updated_at',
        ]
