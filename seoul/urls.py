from django.urls import include, path
from . import views

app_name = 'seoul'

urlpatterns = [
    path('',views.index, name='index'),
    path('line',views.line_list, name='line'),
    path('line/<str:line_num>',views.station_list, name='line_station'),
    path('api/v1/path',views.pathfinder)
]