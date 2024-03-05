from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Person


@admin.register(Person)
class PersonAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'name', 'parent', 'birthdate')
    list_display_links = ('indented_title',)
    list_filter = ('parent', 'birthdate', 'level')
    search_fields = ('name',)

    def indented_title(self, obj):
        return '--> ' * obj.level + str(obj)

    indented_title.short_description = 'Иерархия'

    fieldsets = (
        (None, {'fields': ('name', 'parent', 'birthdate')}),
        ('Изображение', {'fields': ('image',), 'classes': ('collapse',)}),
    )

    readonly_fields = ('indented_title',)
    verbose_name = 'Семья'
    verbose_name_plural = 'Семьи'
