from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelsList, StatusChoicesView, HotelStatusUpdateView, HotelView, UserView, DashboardStats

router = DefaultRouter()
router.register(r'hotels', HotelView)
router.register(r'users', UserView)


urlpatterns = [
    path('super/', include(router.urls)),
    path('super/hotels/', HotelsList.as_view(), name='hotels-list'),
    path('status-choices/', StatusChoicesView.as_view(), name='hotel-status-choices'),
    path('hotel/<int:pk>/status/', HotelStatusUpdateView.as_view(), name='update-hotel-status'),
    path('super/statitics/', DashboardStats.as_view(), name='statitics'),
]
