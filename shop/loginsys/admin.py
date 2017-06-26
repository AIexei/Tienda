from django.contrib import admin
from .models import *

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_nick', 'get_name')
    filter_horizontal = ('favourites',)
    search_fields = ('name',)

    def get_nick(self, obj):
        return obj.user.username

    def get_name(self, obj):
        return ' '.join((obj.user.first_name, obj.user.last_name))

    get_nick.short_description = 'Email(nick)'
    get_name.short_description = 'Name'


admin.site.register(UserProfile, UserProfileAdmin)