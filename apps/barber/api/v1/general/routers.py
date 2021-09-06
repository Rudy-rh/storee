from django.urls import path, include

# THIRD PARTY
from rest_framework.routers import DefaultRouter

# LOCAL
from .stat.views import StatAPIView
from .barberman.views import BarbermanApiView
from .style.views import StyleApiView, StyleOfTheYearApiView
from .brochure.views import BrochureApiView
from .rules.views import RulesApiView
from .branch.views import BranchApiView
from .standard.views import GroupApiView
from .banner.views import BannerApiView
from .information.views import InformationApiView

# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=True)
router.register('barbermans', BarbermanApiView, basename='barberman')
router.register('styles', StyleApiView, basename='style')
router.register('styles-oty', StyleOfTheYearApiView, basename='style_oty')
router.register('brochures', BrochureApiView, basename='brochure')
router.register('rules', RulesApiView, basename='rules')
router.register('groups', GroupApiView, basename='group')
router.register('branchs', BranchApiView, basename='branch')
router.register('banners', BannerApiView, basename='banner')
router.register('informations', InformationApiView, basename='information')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('stats/', StatAPIView.as_view(), name='stat')
]
