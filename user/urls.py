from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm
# Create your views here.
app_name='user'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/',auth_views.LoginView.as_view(template_name='user/login.html',authentication_form=LoginForm), name='login'),
    path('logout/',views.logoutUser,name="logout"),
]


