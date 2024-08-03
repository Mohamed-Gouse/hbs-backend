from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WishlistView, SelectionView, BookingViewSet, WriteReview, search_hotels

router = DefaultRouter()
router.register(r'wishlist', WishlistView)
router.register(r'selection', SelectionView)
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('user/', include(router.urls)),
    path('user/review-add/', WriteReview.as_view()),
    path('search/', search_hotels, name='search_hotels'),
]
