from django.db import models

# Create your models here.
class Station(models.Model):
    line_num = models.CharField(max_length=3)
    station_cd = models.CharField(max_length=4, primary_key=True)
    station_nm = models.CharField(max_length=20)
    fr_code = models.CharField(max_length=5)