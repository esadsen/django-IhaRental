from django.urls import path
from . import views
from .views import drone_list, drone_data, drone_rent, user_rentals, user_rentals_data, rental_delete, rental_update


app_name="rental"

urlpatterns=[
    path('drone/new/',views.new,name='new'),
    path('drone/<int:pk>/edit/',views.edit, name="edit"),
    path('drone/<int:pk>/delete/',views.delete, name="delete"),
    path('drones/', drone_list, name='drone_list'),
    path('drones/data/', drone_data, name='drone_data'),
    path('drone/<int:pk>/rent/', drone_rent, name='drone_rent'),
    path('rentals/', user_rentals, name='user_rentals'),
    path('rentals/data/', user_rentals_data, name='user_rentals_data'),
    path('<int:pk>/edit/', rental_update, name='rental_update'),
    path('<int:pk>/delete/', rental_delete, name='rental_delete'),





    
    
]