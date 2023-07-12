from django.contrib import admin
from django.urls import path, include
from core import routing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('ws/', include(routing.websocket_urlpatterns)),
]
