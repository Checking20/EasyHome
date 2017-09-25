from django.conf.urls import url
from . import views

urlpatterns = [
    #测试的url
    url(r'^helloworld/$', views.Helloworld),
    url(r'^hello/message=(?P<message>.+)/$',views.Hello),
    #房间占用情况
    url(r'^roomOccupancyRate/hotel=(?P<hotel>.+)/$', views.RoomOccupancyRate),
    #查看某天收入情况
    url(r'^hotelRevenue/date=(?P<date>[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])&hotel=(?P<hotel>.+)/$', views.Revenue),
    #
    url(r'^customerRoomType/hotel=(?P<hotel>.+)/$', views.CustomerRoomType),
    #查看用户账户金额是否正确
    url(r'^checkup/username=(?P<username>.+)/$', views.Checkup),
    #退房
    url(r'^checkout/checkInID=(?P<checkinid>[0-9]+)/$', views.Checkout),
    #换房
    url(r'^change/roomID=(?P<roomid>.+)&checkInID=(?P<checkinid>[0-9]+)/$', views.change)
]