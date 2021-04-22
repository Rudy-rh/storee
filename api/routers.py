from django.urls import path, include
from api.views import RootApiView
from apps.person.api.v1 import routers as person_routers

urlpatterns = [
    path('', RootApiView.as_view(), name='api'),
    path('person/v1/', include((person_routers, 'person_api'), namespace='person_v1')),
]
