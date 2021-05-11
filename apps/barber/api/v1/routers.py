from django.urls import path, include
from .customer import routers as customer_routers
from .general import routers as general_routers

urlpatterns = [
    path('customer/', include((customer_routers, 'customer'))),
    path('general/', include((general_routers, 'general'))),
]
