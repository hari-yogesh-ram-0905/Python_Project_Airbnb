from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Review.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)

    @action(detail=False, methods=['get'])
    def listing_reviews(self, request):
        """Get all reviews for a specific listing"""
        listing_id = request.query_params.get('listing_id')
        if not listing_id:
            return Response({"error": "listing_id is required"}, status=400)
        
        reviews = Review.objects.filter(listing_id=listing_id)
        serializer = self.get_serializer(reviews, many=True)
        avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return Response({
            "reviews": serializer.data,
            "average_rating": avg_rating or 0,
            "total_reviews": reviews.count()
        })

    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """Get all reviews written by the logged-in user"""
        reviews = Review.objects.filter(guest=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
