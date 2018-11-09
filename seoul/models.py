from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Station(models.Model):
    class Meta:
        ordering = ['fr_code']
    STATION_NUM_CHOICES = [
        ('1', '1호선'),
        ('2', '2호선'),
        ('3', '3호선'),
        ('4', '4호선'),
        ('5', '5호선'),
        ('6', '6호선'),
        ('7', '7호선'),
        ('8', '8호선'),
        ('9', '9호선'),
        ('A','공항철도'),
        ('B','분당선'),
        ('E','전대에버라인'),
        ('G','경춘선'),
        ('I','인천1호선'),
        ('I2','인천2호선'),
        ('K','경의중앙선'),
        ('KK','경강선'),
        ('S','신분당선'),
        ('SU','수인선'),
        ('T','테스트'),
        ('U','의정부경전철'),
        ('UI','우이신설선')
    ]
    index = models.IntegerField()
    line_num = models.CharField(
        max_length=3,
        choices=STATION_NUM_CHOICES
    )
    station_cd = models.CharField(max_length=4, primary_key=True)
    station_nm = models.CharField(max_length=20)
    fr_code = models.CharField(max_length=5)
    transfer_count = models.IntegerField(default=1)
    naver_cd = models.CharField(max_length=10, default='', blank=True)
    head_station = models.ForeignKey('self', on_delete=models.CASCADE, default='', related_name= 'head_station_set')
    tail_station = models.ForeignKey('self', on_delete=models.CASCADE, default='', related_name= 'tail_station_set')
    head_time = models.FloatField(null=True)
    tail_time = models.FloatField(null=True)
    tag_count = models.IntegerField(default=0)

    def __str__(self):
        return self.station_nm + '({})'.format(self.line_num)


class Spot(models.Model):
    station = models.ForeignKey(
        'Station',
        on_delete=models.CASCADE,
        default= 'T123'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CheckIn(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    spots = models.ManyToManyField(Spot, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_checkin(sender,instance, created, **kwargs):
    if created:
        CheckIn.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_checkin(sender, instance, **kwargs):
    instance.checkin.save()
