from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import WishlistSerializer, SelectionSerializer, BookingSerializer, ReviewSerializer
from .models import Wishlist, Selections, Review
from hotel_side.models import Hotel, Booking, Room
from django.core.exceptions import ValidationError
import stripe
from django.db.models import Q


stripe.api_key = 'sk_test_51PZB3hHUq15j5kNH49RUpBczC3FsAMxWhmAxvKgzNUn0aShp5TqNdQd6YMqMoTN5msIN8BgQ7M8Hss1bKW0heB3S00F1A3E21f'


class WishlistView(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Wishlist.objects.none()

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        hotel_id = request.data.get('hotel')

        if not hotel_id:
            return Response({"error": "Hotel ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        if Wishlist.objects.filter(user=user, hotel_id=hotel_id).exists():
            return Response({"error": "This hotel is already in your wishlist."}, status=status.HTTP_400_BAD_REQUEST)

        hotel = get_object_or_404(Hotel, id=hotel_id)
        wishlist_entry = Wishlist.objects.create(user=user, hotel=hotel)
        
        serializer = self.get_serializer(wishlist_entry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class SelectionView(viewsets.ModelViewSet):
    serializer_class = SelectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Selections.objects.none()

    def get_queryset(self):
        return Selections.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        room_id = request.data.get('room')
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({'detail': 'Room does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has another active selection
        active_selections = Selections.objects.filter(user=user, status='active')
        if active_selections.exists():
            # Ensure the room's hotel is the same as the one of active selections
            if active_selections.exclude(hotel=room.hotel).exists():
                return Response({'detail': 'You can only select rooms from the same hotel.'}, status=status.HTTP_400_BAD_REQUEST)

        if Selections.objects.filter(user=user, room_id=room_id).exists():
            return Response({'detail': 'Room already in selection'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        check_in = request.data.get('check_in_date')
        check_out = request.data.get('check_out_date')
        room_ids = request.data.get('rooms')

        for room_id in room_ids:
            overlapping_bookings = Booking.objects.filter(Q(rooms__id=room_id, check_in_date=check_in, check_out_date=check_out) | Q(is_active=True))

            if overlapping_bookings.exists():
                room = Selections.objects.filter(user=self.request.user, room__id=room_id).delete()
                return Response({"error": f"Room {room_id} is already booked or reserved for the selected dates."}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        payment_response = self.stripe_checkout_session(booking)

        return Response(payment_response, status=status.HTTP_201_CREATED)


    def stripe_checkout_session(self, booking):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': booking.hotel.name,
                            'description': booking.hotel.description,
                        },
                        'unit_amount': int(booking.total * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                # success_url='https://hotel-booking-system-v1n6.onrender.com/success?session_id={{CHECKOUT_SESSION_ID}}&booking_id={booking.id}',
                # cancel_url='https://hotel-booking-system-v1n6.onrender.com/',
                success_url=f'http://localhost:5173/success?session_id={{CHECKOUT_SESSION_ID}}&booking_id={booking.id}',
                cancel_url='http://localhost:5173/',
            )
            booking.payment_intent = session.payment_intent
            booking.booking_id = f"booking_{booking.id}"
            booking.save()
            selection_instance = Selections.objects.filter(user=booking.user).delete()

            return {
                "session_id": session.id,
                "total_price": booking.total,
                "booking_id": booking.booking_id,
            }
        except Exception as e:
            return {"error": str(e)}
        
    @action(detail=False, methods=['post'], url_path='confirm_payment')
    def confirm_payment(self, request, *args, **kwargs):
        session_id = request.data.get('session_id')
        booking_id = request.data.get('booking_id')
        
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            payment_intent = session.payment_intent
            
            booking = get_object_or_404(Booking, id=booking_id)
            booking.payment_status = 'paid'
            booking.payment_intent = payment_intent
            booking.save()

            return Response({'status': 'Payment confirmed and booking updated'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
class WriteReview(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  
