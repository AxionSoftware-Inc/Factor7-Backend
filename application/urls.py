from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, TagViewSet, TourViewSet, 
    BookingViewSet, InquiryViewSet, DashboardStatsAPI, UserViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'tours', TourViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'inquiries', InquiryViewSet)
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('admin-dashboard-stats/', DashboardStatsAPI.as_view(), name='admin-dashboard-stats'),
    path('', include(router.urls)),
]
