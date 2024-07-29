from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListHotels, CheckAvailabilityView, ListSelections, UserView, UserEditView, BookingList, WishlistView

router = DefaultRouter()
router.register(r'hotels', ListHotels)
router.register(r'selections', ListSelections)
router.register(r'bookings', BookingList)
router.register(r'wishlists', WishlistView)

urlpatterns = [
    path('users/', include(router.urls)),
    path('check-availability/', CheckAvailabilityView.as_view(), name='check-availability'),
    path('users/profile/', UserView.as_view(), name='user-profile'),
    path('users/profile/edit/', UserEditView.as_view(), name='user-profile'),
]
