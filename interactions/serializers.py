from rest_framework import serializers
from .models import Wishlist, Selections, Review
from hotel_side.models import Booking

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
    class Meta:
        model = Booking
        exclude = ['checked_in', 'checked_out', 'is_active']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['review', 'hotel', 'user'] 
        read_only_fields = ['user']
        
