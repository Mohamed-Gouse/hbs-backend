from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, DocumentViewSet, GalleryViewSet, FeatureViewSet, RoomTypeViewSet, RoomViewSet, FAQViewSet, BookingsViewAdmin, ReservationCreateView, ReservationView, HotelReviews, StatisticsAPIView

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'galleries', GalleryViewSet)
router.register(r'features', FeatureViewSet)
router.register(r'room_types', RoomTypeViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'bookings', BookingsViewAdmin)
router.register(r'reservations', ReservationView)
router.register(r'reviews', HotelReviews)

urlpatterns = [
    path('admin/', include(router.urls)),
    path('admin/create-reservation/', ReservationCreateView.as_view(), name='create_reservation'),
    path('admin/statistics/', StatisticsAPIView.as_view(), name='statistics'),
]
