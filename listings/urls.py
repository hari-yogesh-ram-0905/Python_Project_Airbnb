from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, AmenityViewSet

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'amenities', AmenityViewSet, basename='amenity')

urlpatterns = [
    path('', include(router.urls)),
]