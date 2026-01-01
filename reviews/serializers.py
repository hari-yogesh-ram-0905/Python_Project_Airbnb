from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    guest_username = serializers.CharField(source='guest.username', read_only=True)
    listing_title = serializers.CharField(source='listing.title', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'guest',
            'guest_username',
            'listing',
            'listing_title',
            'rating',
            'comment',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'guest', 'guest_username', 'listing_title', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['guest'] = self.context['request'].user
        return super().create(validated_data)
