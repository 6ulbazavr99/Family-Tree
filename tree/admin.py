# admin.py
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Person

@admin.register(Person)
class PersonAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'name', 'parent', 'birthdate', 'gender', 'mid', 'fid')
    list_display_links = ('indented_title',)
    list_filter = ('parent', 'birthdate', 'level', 'gender')
    search_fields = ('name',)

    def indented_title(self, obj):
        return '--> ' * obj.level + str(obj)

    indented_title.short_description = 'Иерархия'

    fieldsets = (
        (None, {'fields': ('name', 'parent', 'birthdate', 'gender', 'mid', 'fid')}),
        ('Изображение', {'fields': ('image',), 'classes': ('collapse',)}),
    )

    readonly_fields = ('indented_title',)
    verbose_name = 'Человек'
    verbose_name_plural = 'Люди'

    def get_children_data(self, obj):
        children_data = super().get_children_data(obj)
        for child_data in children_data:
            child_data['title'] = None
        return children_data
