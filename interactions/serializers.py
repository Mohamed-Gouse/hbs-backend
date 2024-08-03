from rest_framework import serializers
from .models import Wishlist, Selections, Review
from hotel_side.models import Booking, Room, Hotel

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'
        read_only_fields = ['user']

class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selections
        fields = '__all__'
        read_only_fields = ['total_days']

class BookingSerializer(serializers.ModelSerializer):
    rooms = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), many=True)
    class Meta:
        model = Booking
        exclude = ['checked_in', 'checked_out', 'is_active']

    def create(self, validated_data):
        rooms = validated_data.pop('rooms')
        booking = Booking.objects.create(**validated_data)
        booking.rooms.set(rooms)
        return booking

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['review', 'hotel', 'user'] 
        read_only_fields = ['user']

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

