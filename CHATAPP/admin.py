from django.contrib import admin
from .models import *

admin.site.register(profile)
admin.site.register(reset_password)
admin.site.register(chatroom)
admin.site.register(chat_message)