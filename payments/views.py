import stripe
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Payment
from .serializers import PaymentSerializer
from bookings.models import Booking

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Payment.objects.filter(booking__guest=user) | Payment.objects.filter(booking__listing__host=user)

    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        """Process payment using Stripe"""
        payment = self.get_object()
        
        if payment.booking.guest != request.user:
            return Response(
                {"error": "You can only pay for your own bookings"},
                status=status.HTTP_403_FORBIDDEN
            )

        if payment.status != 'pending':
            return Response(
                {"error": f"Payment is already {payment.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = request.data.get('stripe_token')
            if not token:
                return Response(
                    {"error": "stripe_token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create Stripe charge
            charge = stripe.Charge.create(
                amount=int(payment.amount * 100),  # Convert to cents
                currency='usd',
                source=token,
                description=f"Payment for {payment.booking.listing.title}"
            )

            # Update payment status
            payment.status = 'completed'
            payment.stripe_payment_intent = charge.id
            payment.transaction_id = charge.id
            payment.save()

            # Update booking status
            payment.booking.status = 'confirmed'
            payment.booking.save()

            return Response(
                self.get_serializer(payment).data,
                status=status.HTTP_200_OK
            )

        except stripe.error.CardError as e:
            payment.status = 'failed'
            payment.save()
            return Response(
                {"error": f"Card error: {e.user_message}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except stripe.error.StripeException as e:
            payment.status = 'failed'
            payment.save()
            return Response(
                {"error": f"Stripe error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """Refund a payment"""
        payment = self.get_object()

        if payment.booking.listing.host != request.user:
            return Response(
                {"error": "Only the host can refund payments"},
                status=status.HTTP_403_FORBIDDEN
            )

        if payment.status != 'completed':
            return Response(
                {"error": "Only completed payments can be refunded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            stripe.Refund.create(charge=payment.stripe_payment_intent)
            payment.status = 'refunded'
            payment.save()
            return Response(
                self.get_serializer(payment).data,
                status=status.HTTP_200_OK
            )
        except stripe.error.StripeException as e:
            return Response(
                {"error": f"Refund error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def webhook(self, request):
        """Handle Stripe webhooks"""
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return Response(
                {"error": "Invalid payload"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except stripe.error.SignatureVerificationError:
            return Response(
                {"error": "Invalid signature"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if event['type'] == 'charge.succeeded':
            charge = event['data']['object']
            # Handle successful charge
            pass

        return Response({"status": "received"}, status=status.HTTP_200_OK)
