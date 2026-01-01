from rest_framework import serializers
from .models import Message, Conversation


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'sender_username',
            'receiver',
            'receiver_username',
            'content',
            'is_read',
            'created_at',
        ]
        read_only_fields = ['id', 'sender', 'sender_username', 'receiver_username', 'created_at']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=serializers.SerializerMethodField(),
        write_only=True,
        many=True,
        source='participants'
    )

    class Meta:
        model = Conversation
        fields = [
            'id',
            'participants',
            'participant_ids',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'participants', 'created_at', 'updated_at']
