from django.urls import path
from api.v1.messages.views import MessageList

urlpatterns = [
    path('', MessageList.as_view()),
]
