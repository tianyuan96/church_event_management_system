from django.contrib import admin
from .models import Event, Post, ReplyTo
# Register your models here.

admin.site.register(Event)
admin.site.register(Post)
admin.site.register(ReplyTo)