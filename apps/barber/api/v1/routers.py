from django.urls import path, include

# THIRD PARTY
from rest_framework.routers import DefaultRouter

# LOCAL
from .barberman.views import BarbermanApiView
from .style.views import StyleApiView
from .booking.views import BookingApiView

# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=True)
router.register('barbermans', BarbermanApiView, basename='barberman')
router.register('styles', StyleApiView, basename='style')
router.register('bookings', BookingApiView, basename='booking')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
