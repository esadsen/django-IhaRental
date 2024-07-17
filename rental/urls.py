from django.urls import path
from . import views
from .views import drone_list, drone_data


app_name="rental"

urlpatterns=[
    path('drone/new/',views.new,name='new'),
    path('drone/<int:pk>/edit/',views.edit, name="edit"),
    path('drone/<int:pk>/delete/',views.delete, name="delete"),
    path('drones/', drone_list, name='drone_list'),
    path('drones/data/', drone_data, name='drone_data'),




    
    
]