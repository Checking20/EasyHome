from django.contrib import admin
from .models import Hotel, RoomType, Room, HotelManagerProfile, HotelReceptionProfile, CustomerProfile, BookingRoom, CheckIn, CustomerProfile

# Register your models here.
#admin.site.register(HotelManager)
'''
class ProfileInline(admin.StackedInline):  #将UserProfile加入到Admin的user表中
    model = CustomerProfile
    verbose_name = 'profile'

class CustomerProfileAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)
'''

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(HotelReceptionProfile)
admin.site.register(HotelManagerProfile)
admin.site.register(CustomerProfile)
admin.site.register(BookingRoom)
admin.site.register(CheckIn)
