from django.urls import path, include
from .v1 import routers

urlpatterns = [
    path('barber/v1/', include((routers, 'barber_api'), namespace='barber_api')),
]
