from django.urls import path, include
from api.views import RootApiView, ping
from apps.person.api.v1 import routers as person_routers
from apps.barber.api.v1 import routers as barber_routers

urlpatterns = [
    path('', RootApiView.as_view(), name='api'),
    path('ping/', ping, name='ping'),
    path('person/v1/', include((person_routers, 'person_api'), namespace='person_v1')),
    path('barber/v1/', include((barber_routers, 'barber_api'), namespace='barber_v1')),
]
