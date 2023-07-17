from django.contrib import admin
from django.urls import path, include

from core import routing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include(routing.websocket_urlpatterns)),
]
