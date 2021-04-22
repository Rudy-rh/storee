from django.urls import path

# LOCAL
from .generator.views import PingApiView


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('ping/', PingApiView.as_view(), name='ping'),
]
