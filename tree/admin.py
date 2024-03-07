from django.contrib import admin
from django.contrib.auth.models import Group, User
from mptt.admin import DraggableMPTTAdmin
from .models import Person


@admin.register(Person)
class PersonAdmin(DraggableMPTTAdmin):
    list_display = ('indented_title', 'name', 'parent', 'fid', 'mid', 'get_pids', 'birthdate', 'gender')
    list_display_links = ('indented_title',)
    list_filter = ('parent', 'birthdate', 'gender')
    search_fields = ('name',)

    def indented_title(self, obj):
        level = obj.level if obj.level is not None else 0
        return '--> ' * level + str(obj)

    def get_pids(self, obj):
        return ', '.join([str(pid) for pid in obj.pids.all()])

    get_pids.short_description = 'Партнеры'
    indented_title.short_description = 'Иерархия'

    fieldsets = (
        ('Иерархия', {'fields': ('indented_title',)}),
        ('Персональные данные', {'fields': ('name', 'birthdate', 'gender')}),
        ('Семейная связь', {'fields': ('parent', 'fid', 'mid', 'pids')}),
        ('Изображение', {'fields': ('img',), 'classes': ('collapse',)}),
    )

    readonly_fields = ('indented_title',)
    verbose_name = 'Человек'
    verbose_name_plural = 'Люди'


admin.site.site_header = "Семейное древо"
admin.site.unregister(Group)
admin.site.unregister(User)
