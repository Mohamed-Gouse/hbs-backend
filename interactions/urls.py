from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WishlistView, SelectionView, BookingViewSet, WriteReview

router = DefaultRouter()
router.register(r'wishlist', WishlistView)
router.register(r'selection', SelectionView)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('user/', include(router.urls)),
    path('user/review-add/', WriteReview.as_view()),
]
