from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from .models import Listing, Amenity
from .serializers import ListingSerializer, AmenitySerializer
from rest_framework.exceptions import PermissionDenied



class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [AllowAny]


# class ListingViewSet(viewsets.ModelViewSet):
#     queryset = Listing.objects.all()
#     serializer_class = ListingSerializer
#     permission_classes = [AllowAny]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['title', 'location', 'description']
#     ordering_fields = ['price_per_night', 'created_at']

#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'destroy']:
#             permission_classes = [IsAuthenticated]
#         else:
#             permission_classes = [AllowAny]
#         return [permission() for permission in permission_classes]

#     def perform_create(self, serializer):
#         serializer.save(host=self.request.user)

#     def perform_update(self, serializer):
#         if serializer.instance.host != self.request.user:
#             return Response(
#                 {"error": "You can only edit your own listings"},
#                 status=status.HTTP_403_FORBIDDEN
#             )
#         serializer.save()

#     def perform_destroy(self, instance):
#         if instance.host != self.request.user:
#             return Response(
#                 {"error": "You can only delete your own listings"},
#                 status=status.HTTP_403_FORBIDDEN
#             )
#         instance.delete()

#     @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
#     def my_listings(self, request):
#         """Get all listings created by the logged-in user"""
#         if not request.user.is_authenticated:
#             return Response(
#                 {"error": "Authentication required"},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
#         listings = Listing.objects.filter(host=request.user)
#         serializer = self.get_serializer(listings, many=True)
#         return Response(serializer.data)

#     @action(detail=False, methods=['get'])
#     def search(self, request):
#         """Search listings by location, price range, and availability"""
#         location = request.query_params.get('location', '').strip()
#         min_price_param = request.query_params.get('min_price', None)
#         max_price_param = request.query_params.get('max_price', None)
#         max_guests_param = request.query_params.get('max_guests', None)

#         queryset = Listing.objects.filter(is_available=True)

#         if location:
#             queryset = queryset.filter(location__icontains=location)

#         # parse min_price only if provided and non-empty
#         if min_price_param is not None and str(min_price_param).strip() != '':
#             try:
#                 min_price = float(min_price_param)
#                 queryset = queryset.filter(price_per_night__gte=min_price)
#             except (ValueError, TypeError):
#                 pass

#         # parse max_price only if provided and non-empty and not the string 'inf'
#         if max_price_param is not None and str(max_price_param).strip() != '' and str(max_price_param).lower() != 'inf':
#             try:
#                 max_price = float(max_price_param)
#                 queryset = queryset.filter(price_per_night__lte=max_price)
#             except (ValueError, TypeError):
#                 pass

#         if max_guests_param is not None and str(max_guests_param).strip() != '':
#             try:
#                 max_guests = int(max_guests_param)
#                 queryset = queryset.filter(max_guests__gte=max_guests)
#             except (ValueError, TypeError):
#                 pass

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

# --------------------------------------------------------------------------




class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'location', 'description']
    ordering_fields = ['price_per_night', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'my_listings']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.host != self.request.user:
            raise PermissionDenied("You can only edit your own listings")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.host != self.request.user:
            raise PermissionDenied("You can only delete your own listings")
        instance.delete()

    @action(
        detail=False,
        methods=['get'],
        url_path='my-listings',
        url_name='my-listings'
    )
    def my_listings(self, request):
        listings = Listing.objects.filter(host=request.user)
        serializer = self.get_serializer(listings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        location = request.query_params.get('location', '').strip()
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        max_guests = request.query_params.get('max_guests')

        queryset = Listing.objects.filter(is_available=True)

        if location:
            queryset = queryset.filter(location__icontains=location)

        if min_price:
            try:
                queryset = queryset.filter(price_per_night__gte=float(min_price))
            except ValueError:
                pass

        if max_price and str(max_price).lower() != 'inf':
            try:
                queryset = queryset.filter(price_per_night__lte=float(max_price))
            except ValueError:
                pass

        if max_guests:
            try:
                queryset = queryset.filter(max_guests__gte=int(max_guests))
            except ValueError:
                pass

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
