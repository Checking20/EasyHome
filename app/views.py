from django.shortcuts import render, render_to_response

# Create your views here.
import django_filters

from django import forms

from django.http import request, HttpResponse, HttpResponseRedirect

from rest_framework import authentication, permissions, viewsets, filters

from rest_framework.decorators import api_view

from rest_framework.response import Response

from rest_framework.views import APIView

from django.db import transaction

from .models import HotelManager, Hotel, RoomType, Room, CustomerProfile, HotelManagerProfile, HotelReceptionProfile, \
    BookingRoom, CheckIn

from .serializers import UserSerializer, RoomTypeSerializer, HotelSerializer, RoomSerializer, BookingRoomSerializer,CheckInSerializer

from django.contrib.auth import get_user_model, authenticate

from django.views.decorators.csrf import csrf_exempt

import datetime,time

User = get_user_model()


class DefaultMixin(object):
    # 默认的视图设置
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (
        # permissions.IsAuthenticated,
    )

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100


'''class HotelManagerViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = HotelManager.objects.all()
    serializer_class = HotelManagerSerializer
'''

'''modelviewset'''


# 宾馆模型视图
class HotelFilter(django_filters.FilterSet):
    class Meta:
        model = Hotel
        fields = ('city', 'hotelName',)


class RoomFilter(django_filters.FilterSet):
    class Meta:
        model = Room
        fields = ('roomID', 'type',)


# 用户模型视图
class UserViewSet(DefaultMixin, viewsets.ModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
    search_fields = (User.USERNAME_FIELD,)


'''
class CustomerProfileViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
'''


class RoomViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_class = RoomFilter
    search_fields = ('roomID',)


# 房型的视图模型
class RoomTypeViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    search_fields = ('hotelName',)


# 宾馆的视图模型
class HotelViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_class = HotelFilter
    search_fields = ('city', 'hotelName')


# 预定的视图模型
class BookingRoomViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = BookingRoom.objects.all()
    serializer_class = BookingRoomSerializer
    search_fields = ('hotelName', 'customerUser')


# 入住的视图模型
class CheckInViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    search_fields = ('customerName','customerUser')


'''view'''


# 以下两个函数是测试
@api_view()
def Helloworld(request):
    return Response({"message": "Hello, world!"})


@api_view()
def Hello(request, message):
    return Response({"message": message})


# 用户看到的房型信息
@api_view()
# @transaction.commit_on_success
def CustomerRoomType(request, hotel):
    roomtypes = RoomType.objects.filter(hotelName=hotel)
    list=[]
    for e in roomtypes:
        # 该房型的剩余数量
        rooms = Room.objects.filter(hotelName=hotel, roomStatus='F', type=e)
        # 该房型的预定数量
        rooms_booked = BookingRoom.objects.filter(hotelName=hotel, TypeName=e)
        print("%s: %d %d" % (e.TypeName, rooms.count(), rooms_booked.count()))
        total = 0;
        # 预定数x总数
        for ee in rooms_booked:
            total += ee.bookingNum
        #直接返回值有些不好
        list.append({'typeName': e.TypeName,'description': e.description,'remainingNumble': rooms.count() - total, 'typeID': e.id, })
        #print(list)
    return Response(list)


# 某酒店当前入住率
@api_view()
# @transaction.commit_on_success
def RoomOccupancyRate(request, hotel):
    roomsAll = Room.objects.filter(hotelName=hotel)
    rooms = Room.objects.filter(hotelName=hotel, roomStatus='U')
    print(roomsAll.count(), rooms.count())
    if roomsAll.count():
        return Response({"hotelName": hotel, "OccupancyRate": rooms.count() / roomsAll.count()})
    else:
        # 该酒店房间数为0或者没有该酒店
        return Response({"hotelName": hotel, "OccupancyRate": 0})


# 某酒店某天的收入信息
@api_view()
def Revenue(request, hotel, date):
    date = datetime.datetime.strptime(date,'%Y-%m-%d').date()
    print(date)
    hotel = Hotel.objects.get(hotelName=hotel)
    checkins=CheckIn.objects.filter(hotelName=hotel)
    total=0
    for e in checkins:
        if e.status=='L' and e.leaveTime.date()==date:
            room = Room.objects.get(roomID=e.roomID.roomID, hotelName=e.hotelName)
            roomtype = RoomType.objects.get(TypeName=room.type.TypeName, hotelName=e.hotelName.hotelName)
            span = int(str(e.leaveTime.date() - e.checkInTime.date()).split(' ')[0])
            total += roomtype.price * span
    return Response({'date': date,'revenue': total,})

# 前台为客户退房
@api_view()
# @transaction.commit_on_success
def Checkout(request, checkinid):
    # 根据用户id得到对应入住表单
    checkin = CheckIn.objects.get(checkInID=checkinid)
    # 修改入住表信息
    print(checkin.status)
    checkin.status = 'L'
    checkin.save()
    # 修改房间信息
    room = Room.objects.get(roomID=checkin.roomID.roomID, hotelName=checkin.hotelName)
    print(room.roomStatus)
    room.roomStatus = 'F'
    room.save()
    # 为顾客用户添加消费,实际上类似账本的机制
    cuser = CustomerProfile.objects.get(user=checkin.customerUser)
    roomtype = RoomType.objects.get(TypeName=room.type.TypeName, hotelName=checkin.hotelName.hotelName)
    cuser.consumption = cuser.consumption + roomtype.price
    span = int(str(checkin.leaveTime.date() - checkin.checkInTime.date()).split(' ')[0])
    print(cuser.consumption + roomtype.price*span)
    cuser.save()
    return Response()


# 查询顾客用户的消费是否属实
@api_view()
# @transaction.commit_on_success
def Checkup(request, username):
    user = User.objects.get(username=username)
    user = CustomerProfile.objects.get(user=user)
    checkins = CheckIn.objects.filter(customerUser=user)
    total = 0
    tmp=0;
    s = True
    for e in checkins:
        if e.status == 'L':
            room = Room.objects.get(roomID=e.roomID.roomID, hotelName=e.hotelName)
            roomtype = RoomType.objects.get(TypeName=room.type.TypeName, hotelName=e.hotelName.hotelName)
            span = int(str(e.leaveTime.date() - e.checkInTime.date()).split(' ')[0])
            total += roomtype.price*span
    if total != user.consumption:
        print("记账有问题")
        s=False
        tmp=user.consumption
        user.consumption = total
        user.save()
    else:
        tmp=total
        print("记账正确")
        s = True
    return Response({'记录': tmp,'实际': total,'状态': s , })


# 前台为客户换房
@api_view()
# @transaction.commit_on_success
def change(request, roomid, checkinid):
    checkin = CheckIn.objects.get(checkInID=checkinid)
    curroom = Room.objects.get(hotelName=checkin.hotelName, roomID=checkin.roomID.roomID)
    print(curroom)
    targetroom = Room.objects.get(hotelName=checkin.hotelName, roomID=roomid)
    print(targetroom)
    if targetroom and targetroom.roomStatus == 'F':
        targetroom.roomStatus = 'U'
        print(targetroom.roomStatus)
        targetroom.save()
        curroom.roomStatus = 'F'
        print(curroom.roomStatus)
        curroom.save()
        checkin.roomID = targetroom
        checkin.save()
        print("已更换")
    else:
        print("被占用")
    return Response()


'''返回HTTP的视图逻辑'''


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')


# 注册
@csrf_exempt
def regist(request):
    if request.method == 'POST':
        # print(request.POST)
        userform = UserForm(request.POST)
        # print(userform)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            email = userform.cleaned_data['email']
            print("Begin Create New User...")
            if User.objects.filter(username=username):
                return HttpResponse('该用户已存在')
            newuser=User.objects.create(username=username, password=password, email=email)
            CustomerProfile.objects.create(user=newuser)
            return HttpResponse('注册成功')
    else:
        userform = UserForm()
    return render_to_response('regist.html', {'userform': userform})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        print(request.POST)
        userform = UserForm(request.POST)
        print(userform)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            user = User.objects.filter(username=username)
            # 登陆验证
            if authenticate(username=username, password=password):
                # 用户账号是否被冻结
                CS = CustomerProfile.objects.filter(user=user)
                HM = HotelManagerProfile.objects.filter(user=user)
                HR = HotelReceptionProfile.objects.filter(user=user)
                if user[0].is_active:
                    # 用户区分
                    response = HttpResponseRedirect("/welcome/index/")
                    # 添加cookie，并添加失效时间
                    response.set_cookie('username', username, 3600)
                    if CS:
                        print(CS)
                        response.set_cookie('is_Customer', user[0].id, 3600)
                    elif HM:
                        print(HM)
                        response.set_cookie('is_HotelManager', user[0].id, 3600)
                    elif HR:
                        print(HR)
                        response.set_cookie('is_HotelReception', user[0].id, 3600)
                        print('OK')
                    return response
                else:
                    return HttpResponse('该用户已经被冻结')
        else:
            HttpResponse('用户名或密码错误,请重新登陆')
    else:
        userform = UserForm()
    username = request.COOKIES.get('username', '')
    if username:
        return HttpResponseRedirect("/welcome/index/")
    else:
        return render_to_response('login.html', {'userform': userform})


def logout(request):
    response = HttpResponseRedirect("/welcome/login/")
    # 清除cookie
    response.delete_cookie('username')
    response.delete_cookie('is_HotelManager')
    response.delete_cookie('hotelname')
    response.delete_cookie('is_HotelReception')
    response.delete_cookie('is_Customer')
    return response


def index(request):
    # 检查cookie
    username = request.COOKIES.get('username', '')
    if username:
        # cookie中有该用户
        print("Cookie found!")
        if request.COOKIES.get('is_Customer', ''):
            # 是顾客
            return render_to_response('dashboard_CS.html', {'username': username})
        elif request.COOKIES.get('is_HotelManager'):
            # 是酒店经理
            return render_to_response('dashboard_HM.html', {'username': username})
        elif request.COOKIES.get('is_HotelReception'):
            # 是酒店前台
            return render_to_response('dashboard_HR.html', {'username': username})
        else:
            # 什么都不是？
            return HttpResponse("什么类型都不是？难道是BUG")
            # cookie中没有登陆信息，拒绝，回到登陆页面

    else:
        return HttpResponseRedirect("/welcome/login/")
