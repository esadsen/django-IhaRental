from django.urls import path
from . import views

app_name="rental"

urlpatterns=[
    path('new/',views.new,name='new'),
    
    
]