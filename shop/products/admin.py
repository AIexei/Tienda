from django.contrib import admin
from django.contrib.admin.actions import delete_selected as django_delete_selected
from mptt.admin import DraggableMPTTAdmin
from .models import *

# Register your models here.

class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title')
    list_display_links = ('indented_title', )
    mptt_level_indent = 30


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'get_categories')
    ordering = ('name',)
    filter_horizontal = ('categories',)
    search_fields = ('name',)

    def get_categories(self, obj):
        return ' ,'.join(cat.name for cat in obj.categories.all())

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            no_children_objects_ids = []

            for i in Category.objects.all():
                if not i.get_descendant_count():
                    no_children_objects_ids.append(i.id)

            kwargs["queryset"] = Category.objects.filter(id__in=no_children_objects_ids)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    get_categories.short_description = 'Categories'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'owner', 'sku', 'date',)


class SKUAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'color', 'body_material', 'screen_diagonal',
                    'screen_resolution', 'get_ppi', 'weight', 'battery_capacity',)

    ordering = ('stock_id',)
    exclude = ('stock_id',)
    actions = ['delete_selected',]

    def delete_selected(self, request, queryset):
        for obj in queryset:
            obj.image.delete()

        return django_delete_selected(self, request, queryset)

    delete_selected.short_description = django_delete_selected.short_description


admin.site.register(Manufacturer)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(SKU, SKUAdmin)