from django.contrib import admin
from api.v1.models import Conversation, Message

admin.site.register(Conversation)
admin.site.register(Message)
