from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^regist/$', views.regist, name='regist'),
    url(r'^$', views.index),
    url(r'^helloworld/$', views.Helloworld),
]
#router.register(r'generalviews/hotelbook/(?P<homename>[0-9]+)/$', views.RoomTypeDetail)name
