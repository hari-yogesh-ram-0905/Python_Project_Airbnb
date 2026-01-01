from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'host':
            return Booking.objects.filter(listing__host=user)
        else:
            return Booking.objects.filter(guest=user)

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Host confirms a pending booking"""
        booking = self.get_object()
        if booking.listing.host != request.user:
            return Response(
                {"error": "Only the listing host can confirm bookings"},
                status=status.HTTP_403_FORBIDDEN
            )
        if booking.status != 'pending':
            return Response(
                {"error": "Only pending bookings can be confirmed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        booking.status = 'confirmed'
        booking.save()
        return Response(self.get_serializer(booking).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        if booking.guest != request.user and booking.listing.host != request.user:
            return Response(
                {"error": "You cannot cancel this booking"},
                status=status.HTTP_403_FORBIDDEN
            )
        if booking.status == 'cancelled':
            return Response(
                {"error": "Booking is already cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        booking.status = 'cancelled'
        booking.save()
        return Response(self.get_serializer(booking).data)

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """Get all bookings for the logged-in user"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
