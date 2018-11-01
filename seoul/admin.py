from django.contrib import admin
from .models import Station, Spot, CheckIn

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'line_num', 'station_cd', 'fr_code','head_station_f', 'tail_station_f')
    list_filter = ('line_num',)
    search_fields = ('station_nm',)


    def head_station_f(self, station):
        return station.head_station


    def tail_station_f(self, station):
        return station.tail_station




admin.site.register(Spot)
admin.site.register(CheckIn)


# Register your models here.
