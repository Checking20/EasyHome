from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
#router.register(r'hotelManager', views.HotelManagerViewSet)
#router.register(r'customer', views.CustomerProfileViewSet)
router.register(r'roomType', views.RoomTypeViewSet)
router.register(r'hotel', views.HotelViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'room', views.RoomViewSet)
router.register(r'bookingRoom', views.BookingRoomViewSet)
router.register(r'checkIn', views.CheckInViewSet)
#router.register()