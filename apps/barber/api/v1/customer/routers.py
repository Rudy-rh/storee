from django.urls import path, include

# THIRD PARTY
from rest_framework.routers import DefaultRouter

# LOCAL
from .booking.views import BookingApiView

# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=True)
router.register('bookings', BookingApiView, basename='booking')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
