from .serializers import BookingSerializer, HotelSerializer, CheckAvailabilitySerializer, RoomSerializer, SelectionListSerializer, UserSerializer, WishlistSerializer
from hotel_side.models import Hotel, Room, Room_type, Booking, Reservation
from interactions.models import Selections, Wishlist
from rest_framework import viewsets, permissions, generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from datetime import timedelta, date


class ListHotels(viewsets.ModelViewSet):
    serializer_class = HotelSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Hotel.objects.filter(status="approved")
    lookup_field = 'slug'

class CheckAvailabilityView(generics.GenericAPIView):
    serializer_class = CheckAvailabilitySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        check_in = serializer.validated_data['check_in']
        check_out = serializer.validated_data['check_out']
        room_type_id = serializer.validated_data['room_type_id']
        guests = serializer.validated_data['guests']

        room_type = get_object_or_404(Room_type, id=room_type_id)

        if guests > room_type.room_capacity:
            return Response({"error": "Number of guests exceeds room capacity."}, status=status.HTTP_400_BAD_REQUEST)
        
        if check_in >= check_out:
            return Response({"error": "Check-out date must be after check-in date."}, status=status.HTTP_400_BAD_REQUEST)

        if check_out - check_in < timedelta(days=1):
            return Response({"error": "There must be at least one day difference between check-in and check-out."}, status=status.HTTP_400_BAD_REQUEST)

        if check_in < date.today():
            return Response({"error": "Check-in date must be today or a future date."}, status=status.HTTP_400_BAD_REQUEST)

        rooms = Room.objects.filter(room_type=room_type, is_available=True)

        available_rooms = []
        for room in rooms:
            is_booked_or_reserved = Booking.objects.filter(
                rooms=room,
                check_in_date=check_in,
                check_out_date=check_out,
            ).exists() or Reservation.objects.filter(
                room=room,
                check_in_date__gte=check_in,
                check_out_date__lte=check_out,
            ).exists()

            if not is_booked_or_reserved:
                available_rooms.append(room)

        if available_rooms:
            room_serializer = RoomSerializer(available_rooms, many=True)
            return Response({
                "message": "Rooms available",
                "rooms": room_serializer.data,
            }, status=status.HTTP_200_OK)

        return Response({"error": "No available rooms for the selected dates."}, status=status.HTTP_400_BAD_REQUEST)

class ListSelections(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SelectionListSerializer
    queryset = Selections.objects.none()

    def get_queryset(self):
        return Selections.objects.filter(user=self.request.user)
    
class UserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UserEditView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class BookingList(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookingSerializer
    queryset = Booking.objects.none()

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-date')

class WishlistView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WishlistSerializer
    queryset = Wishlist.objects.none()

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    