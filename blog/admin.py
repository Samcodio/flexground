from django.contrib import admin
from .models import Blog,BlogMedia,Share,Notification
from django.contrib import admin
from .models import UserSettings
admin.site.register(Blog)
admin.site.register(BlogMedia)
admin.site.register(Notification)
admin.site.register(Share)
# Register your models here.



@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_strength', 'enable_notifications', 'theme_preference']
    list_filter = ['account_strength', 'enable_notifications', 'theme_preference']
    search_fields = ['user__username']


