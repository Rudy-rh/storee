from django.urls import path, include
from api.views import RootApiView, ping
from apps.person.api import routers as person_routers
from apps.barber.api import routers as barber_routers

urlpatterns = [
    path('', RootApiView.as_view(), name='api'),
    path('ping/', ping, name='ping'),
    path('', include(person_routers)),
    path('', include(barber_routers)),
]
