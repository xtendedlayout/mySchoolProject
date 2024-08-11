from django.contrib import admin
from .models import User, Announcement
# Register your models here.

admin.site.register(User)
admin.site.register(Announcement)