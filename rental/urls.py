from django.urls import path
from . import views

app_name="rental"

urlpatterns=[
    path('new/',views.new,name='new'),
    path('<int:pk>/edit/',views.edit, name="edit"),
    path('<int:pk>/delete/',views.delete, name="delete"),


    
    
]