from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from auth_app.models import Accounts
from .models import Hotel, Document, Gallery, Feature, Room_type, Room, FAQ, Booking, Reservation
from .serializers import HotelSerializer, DocumentSerializer, GallerySerializer, FeatureSerializer, RoomTypeSerializer, RoomSerializer, FAQSerializer, BookingSerializer, ReservationSerializer, ReservationViewSerializer, ReviewSerializer
from rest_framework.decorators import action
from interactions.models import Review
import stripe
from rest_framework.views import APIView
from django.db.models import Sum

stripe.api_key = 'sk_test_51PZB3hHUq15j5kNH49RUpBczC3FsAMxWhmAxvKgzNUn0aShp5TqNdQd6YMqMoTN5msIN8BgQ7M8Hss1bKW0heB3S00F1A3E21f'

class HotelViewSet(viewsets.ModelViewSet):
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Hotel.objects.none()
    lookup_field = 'slug'

    def get_queryset(self):
        return Hotel.objects.filter(user=self.request.user)

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer

class GalleryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GallerySerializer
    queryset = Gallery.objects.none()

    def get_queryset(self):
        user = self.request.user
        hotel_slug = self.request.query_params.get('hotel_slug')
        if hotel_slug:
            return Gallery.objects.filter(hotel__slug=hotel_slug, hotel__user=user)
        return Gallery.objects.none()

    def create(self, request, *args, **kwargs):
        hotel_slug = request.data.get('hotel')
        hotel = get_object_or_404(Hotel, slug=hotel_slug)
        data = request.data.copy()
        data['hotel'] = hotel.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class FeatureViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FeatureSerializer
    queryset = Feature.objects.none()

    def get_queryset(self):
        user = self.request.user
        hotel_slug = self.request.query_params.get('hotel_slug')
        if hotel_slug:
            return Feature.objects.filter(hotel__slug=hotel_slug, hotel__user=user)
        return Feature.objects.none()

    def create(self, request, *args, **kwargs):
        hotel_slug = request.data.get('hotel')
        hotel = get_object_or_404(Hotel, slug=hotel_slug)
        data = request.data.copy()
        data['hotel'] = hotel.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class RoomTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoomTypeSerializer
    queryset = Room_type.objects.none()

    def get_queryset(self):
        user = self.request.user
        hotel_slug = self.request.query_params.get('hotel_slug')
        if hotel_slug:
            return Room_type.objects.filter(hotel__slug=hotel_slug, hotel__user=user)
        return Room_type.objects.none()

    def create(self, request, *args, **kwargs):
        hotel_slug = request.data.get('hotel')
        hotel = get_object_or_404(Hotel, slug=hotel_slug)
        data = request.data.copy()
        data['hotel'] = hotel.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoomSerializer
    queryset = Room.objects.none()

    def get_queryset(self):
        user = self.request.user
        hotel_slug = self.request.query_params.get('hotel_slug')
        if hotel_slug:
            return Room.objects.filter(hotel__slug=hotel_slug, hotel__user=user)
        return Room.objects.none()

    def create(self, request, *args, **kwargs):
        hotel_slug = request.data.get('hotel')
        room_type_id = request.data.get('room_type')
        
        hotel = get_object_or_404(Hotel, slug=hotel_slug)
        room_type = get_object_or_404(Room_type, id=room_type_id, hotel=hotel)

        data = request.data.copy()
        data['hotel'] = hotel.id
        data['room_type'] = room_type.id
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['patch'], url_path='update-availability')
    def update_availability(self, request, pk=None):
        room = get_object_or_404(Room, pk=pk, hotel__user=request.user)
        is_available = request.data.get('is_available')
        if is_available is not None:
            room.is_available = is_available
            room.save()
            return Response({'status': 'availability updated', 'is_available': is_available})
        else:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FAQSerializer

class BookingsViewAdmin(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookingSerializer
    queryset = Booking.objects.none()

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(hotel__user=user)
    
    @action(detail=True, methods=['patch'])
    def check_in_out(self, request, pk=None):
        booking = self.get_object()
        if not booking.checked_in:
            booking.is_active = True
            booking.checked_in = True
            status_message = 'checked in'
        elif booking.checked_in and not booking.checked_out:
            booking.checked_out = True
            booking.is_active = False
            status_message = 'checked out'
        else:
            return Response({'status': 'already checked out'}, status=status.HTTP_400_BAD_REQUEST)

        booking.save()
        return Response({'status': f"what happend {status_message}"}, status=status.HTTP_200_OK)

class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data.get('email')
        if email:
            user = get_object_or_404(Accounts, email=email)
        else:
            user = self.request.user
        
        check_in_date = serializer.validated_data['check_in_date']
        check_out_date = serializer.validated_data['check_out_date']
        total_days = (check_out_date - check_in_date).days
        payment_status = 'pending'
        
        serializer.save(
            user=user,
            total_days=total_days,
            payment_status=payment_status
        )


class ReservationView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationViewSerializer
    queryset = Reservation.objects.none()

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.filter(hotel__user=user)

    @action(detail=True, methods=['patch'])
    def check_in_out(self, request, pk=None):
        booking = self.get_object()
        if not booking.checked_in:
            booking.is_active = True
            booking.checked_in = True
            booking.payment_status = 'paid'
            status_message = 'checked in'
        elif booking.checked_in and not booking.checked_out:
            booking.checked_out = True
            booking.is_active = False
            status_message = 'checked out'
        else:
            return Response({'status': 'already checked out'}, status=status.HTTP_400_BAD_REQUEST)

        booking.save()
        return Response({'status': f"what happend {status_message}"}, status=status.HTTP_200_OK)

class HotelReviews(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer
    queryset = Review.objects.none()

    def get_queryset(self):
        return Review.objects.filter(hotel__user=self.request.user)
    
class StatisticsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        hotels_count = Hotel.objects.filter(user=user).count()
        bookings_count = Booking.objects.filter(hotel__user=user).count()
        reservations_count = Reservation.objects.filter(hotel__user=user).count()
        customers_count = Booking.objects.filter(hotel__user=user).values('user').distinct().count()
        profit = Booking.objects.filter(hotel__user=user).aggregate(total_profit=Sum('total'))['total_profit'] or 0
        reviews_count = Review.objects.filter(hotel__user=user).count()
        
        statistics = {
            'hotels_count': hotels_count,
            'bookings_count': bookings_count,
            'reservations_count': reservations_count,
            'customers_count': customers_count,
            'profit': profit,
            'reviews_count': reviews_count,
        }

        print(statistics)
        
        return Response(statistics)
