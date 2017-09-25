#
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# from django.utils.translation import ugettext_lazy as _

'''
class User(models.Model):
    # 用户id:integer
    userID = models.AutoField(primary_key=True, null=False)
    # 用户姓名:varchar20
    name = models.CharField(max_length=20, null=False)
    # 电话号码:varchar11
    phoneNumber = models.CharField(min_length=11, max_length=11, blank=False)
    # 累计消费：postiveint
    consumption = models.PositiveIntegerField(default=0)
    # 会员级别:erum
    levelSet = (
        (0, 'NORMAL_USER'),
        (1, 'SILVER_MEMBER'),
        (2, 'GOLD_MEMBER'),
        (3, 'DIAMOND_MEMBER'),
    )
    membershipLevel = models.SmallIntegerField(choices=levelSet, default=0)
    # 密码哈希值:varchar64
    passwordHash = models.CharField(max_length=64, blank=False)

    def __str__(self):
        return self.name
'''

# ModelViewSet　
# 用户扩展


class CustomerProfile(models.Model):
    # 和默认的注册系统产生一一对应关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # 电话号码:varchar11
    phoneNumber = models.CharField(max_length=11, blank=False)
    # 累计消费：postiveint
    consumption = models.PositiveIntegerField(default=0)
    # 会员级别:erum
    levelSet = (
        (0, 'NORMAL_USER'),
        (1, 'SILVER_MEMBER'),
        (2, 'GOLD_MEMBER'),
        (3, 'DIAMOND_MEMBER'),
    )
    membershipLevel = models.SmallIntegerField(choices=levelSet, default=0)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'CustomerUser'


class HotelManagerProfile(models.Model):
    # 和默认的注册系统产生一一对应关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # 所属酒店：外键
    hotelName = models.ForeignKey('Hotel', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'HotelManagerUser'


class HotelReceptionProfile(models.Model):
    # 和默认的注册系统产生一一对应关系
    user = models.OneToOneField(User, on_delete=models.CASCADE,  primary_key=True)
    # 所属酒店：外键
    hotelName = models.ForeignKey('Hotel', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = ' HotelReceptionUser'


class Hotel(models.Model):
    # 宾馆名称:varchar20
    hotelName = models.CharField(max_length=20, blank=False, primary_key=True)
    # 宾馆介绍:text
    hotelIntro = models.TextField(blank=True, default='')
    # 所在市:varchar20
    city = models.CharField(max_length=20, blank=False)
    # 所在区:varchar20
    district = models.CharField(max_length=20, blank=False)
    # 具体地址:varchar20
    detailedAddress = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return self.hotelName


class RoomType(models.Model):
    # 房型：char20
    TypeName = models.CharField(max_length=20, blank=False)
    # 宾馆名称:外键
    hotelName = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    # 价格:PostiveInteger
    price = models.PositiveIntegerField(null=False)
    # 描述:text
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.TypeName

    class Meta:
        unique_together = ('TypeName', 'hotelName')


class Room(models.Model):
    # 房间ID
    roomID = models.PositiveIntegerField(null=False)
    # 宾馆名称
    hotelName = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    # 房型
    type = models.ForeignKey('RoomType', on_delete=models.CASCADE)
    # 房间状态
    statusval = (
        ('F', 'FREE'),
        ('U', 'USING'),
        ('M', 'UNDER_MAINTENANCE'),
    )
    roomStatus = models.CharField(max_length=1, choices=statusval, default='F')

    def __str__(self):
        return str(self.hotelName)+str(self.type)+str(self.roomID)+str(self.roomStatus)

    class Meta:
        unique_together = (
            ('roomID', 'hotelName'),
        )


class BookingRoom(models.Model):
    # 预定ID:主键
    BookingID = models.AutoField(primary_key=True, null=False)
    # 用户
    customerUser = models.ForeignKey('CustomerProfile', on_delete=models.CASCADE)
    # 宾馆名称,不删除
    hotelName = models.ForeignKey('Hotel')
    # 房型,不删除
    TypeName = models.ForeignKey('RoomType')
    # 预定时间
    bookingTime = models.DateTimeField(auto_now_add=True)
    # 这样才能显示和编辑时间
    bookingTime.editable=True
    # 房间数
    bookingNum = models.PositiveIntegerField(null=False)

    def __str__(self):
        return str(self.customerUser)+' 预定 '+str(self.TypeName)+' 在 '+str(self.bookingTime)


class CheckIn(models.Model):
    # 入住id：主键
    checkInID = models.AutoField(primary_key=True, null=False)
    # 宾馆名称
    hotelName = models.ForeignKey('Hotel')
    # 房间ID
    roomID = models.ForeignKey('Room')
    # 入住时间
    checkInTime = models.DateTimeField(auto_now_add=True, null=False)
    # 离开时间
    leaveTime = models.DateTimeField(auto_now=True)

    # 这样才能显示和编辑时间
    checkInTime.editable = True
    leaveTime.editable = True
    # 顾客姓名
    customerName = models.CharField(max_length=20, blank=False)
    # 顾客手机号
    customerPhoneNumber = models.CharField(max_length=20,  blank=False)
    # 顾客证件
    customerIDCard = models.CharField(max_length=18, blank=False)
    # 用户
    customerUser = models.ForeignKey('CustomerProfile', on_delete=models.CASCADE)
    # 状态
    statusval = (
        ('C', 'CHECKED_IN'),
        ('L', 'LEAVED'),
    )
    status = models.CharField(max_length=1, choices=statusval, default='C')

    def __str__(self):
        return str(self.checkInID)+' '+str(self.customerName)+' 入住 '+str(self.roomID)+' 在 '+str(self.checkInTime.date())


# 其他
class HotelManager(models.Model):
    # 用户名
    userName = models.CharField(primary_key=True, max_length=20, blank=False)
    # 密码哈希值
    passwordHash = models.CharField(max_length=64, blank=False)

    def __str__(self):
        return self.userName
