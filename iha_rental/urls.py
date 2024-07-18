from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rental.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('rental/', include('rental.urls')),
    path('', index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

