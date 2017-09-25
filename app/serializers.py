from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import HotelManager,Room,RoomType,Hotel,BookingRoom,CheckIn

from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    links = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', 'links')

    def get_links(self, obj):
        request = self.context['request']
        username = obj.get_username()
        return {
            'self': reverse('user-detail', kwargs={User.USERNAME_FIELD: username}, request=request),
        }


'''
class HotelManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelManager
        fields = ('userName', 'passwordHash',)

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('sprint-detail', kwargs={'pk': obj.pk}, request=request),
     }
'''


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('roomID', 'type', 'hotelName')



class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ('TypeName', 'hotelName', 'price', 'description')


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('hotelName', 'hotelIntro', 'city', 'district', 'detailedAddress')


class BookingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRoom
        fields = ('customerUser', 'hotelName', 'TypeName', 'bookingTime', 'bookingNum')

class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields =('checkInID','hotelName','roomID','customerUser','checkInTime','customerName','status')