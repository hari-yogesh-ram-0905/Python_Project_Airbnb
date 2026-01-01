from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    guest_username = serializers.CharField(source='guest.username', read_only=True)
    listing_title = serializers.CharField(source='listing.title', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'guest',
            'guest_username',
            'listing',
            'listing_title',
            'check_in_date',
            'check_out_date',
            'number_of_guests',
            'total_price',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'guest', 'guest_username', 'listing_title', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['guest'] = self.context['request'].user
        return super().create(validated_data)
