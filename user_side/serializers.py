from rest_framework import serializers
from hotel_side.models import Hotel, Gallery, Feature, FAQ, Room_type, Room, Booking
from interactions.models import Selections, Wishlist, Review
from auth_app.models import Accounts

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['id', 'username', 'email', 'full_name', 'photo']
        read_only_fields = ['id', 'email']

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class Room_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room_type
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    room_type = Room_typeSerializer(read_only=True)
    class Meta:
        model = Room
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'review', 'user']

class HotelSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(read_only=True, many=True)
    features = FeatureSerializer(read_only=True, many=True)
    room_type = Room_typeSerializer(read_only=True, many=True)
    rooms = RoomSerializer(read_only=True, many=True)
    faqs = FAQSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)
    review = ReviewSerializer(read_only=True, many=True, source='review_set')

    class Meta:
        model = Hotel
        fields = '__all__'

class CheckAvailabilitySerializer(serializers.Serializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    room_type_id = serializers.IntegerField()
    guests = serializers.IntegerField()

class SelectionListSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    class Meta:
        model = Selections
        fields = '__all__'
        
class BookedHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    hotel = BookedHotelSerializer(read_only=True)
    rooms = RoomSerializer(read_only=True, many=True)
    class Meta:
        model = Booking
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(read_only=True)
    class Meta:
        model = Wishlist
        fields = '__all__'
