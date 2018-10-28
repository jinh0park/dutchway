from django.contrib import admin
from .models import Station, Spot, CheckIn

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'line_num', 'station_cd', 'fr_code')
    list_filter = ('line_num',)



admin.site.register(Spot)
admin.site.register(CheckIn)


# Register your models here.
