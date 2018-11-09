from django.urls import include, path
from . import views

app_name = 'seoul'

urlpatterns = [
    path('',views.index, name='index'),
    path('filter',views.filter, name='filter'),
    path('api/v1/path',views.pathfinder, name="api_path")
]