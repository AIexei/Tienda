from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import *

# Register your models here.

class MyMPTTAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title')
    list_display_links = ('indented_title', )
    mptt_level_indent = 30


admin.site.register(Category, MyMPTTAdmin)
admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(SKU)