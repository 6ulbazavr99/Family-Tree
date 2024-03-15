from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Person
from django.core.exceptions import ValidationError
from django import forms


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        pids = cleaned_data.get('pids')
        if pids and self.instance in pids.all():
            raise ValidationError("Нельзя связать человека с самим собой.")
        return cleaned_data


class PersonAdminMixin:
    form = PersonForm
    list_display = ('tree_actions', 'indented_title', 'name', 'title', 'birthdate', 'gender', 'get_pids', 'fid', 'mid')
    list_display_links = ('indented_title',)
    list_filter = ('parent', 'birthdate', 'gender')
    search_fields = ('name',)

    def indented_title(self, obj):
        parent_name = obj.parent.name if obj.parent else ''
        if parent_name:
            return f"{parent_name} --> {obj.name}"
        else:
            return obj.name

    indented_title.short_description = 'Иерархия'

    def get_pids(self, obj):
        return ', '.join([str(pid) for pid in obj.pids.all()])

    get_pids.short_description = 'Партнеры'

    fieldsets = (
        ('Иерархия', {'fields': ('indented_title',)}),
        ('Персональные данные', {'fields': ('name', 'title', 'birthdate', 'gender')}),
        ('Семейная связь', {'fields': ('parent', 'fid', 'mid', 'pids')}),
        ('Изображение', {'fields': ('img',), 'classes': ('collapse',)}),
    )

    readonly_fields = ('indented_title',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if 'pids' in form.changed_data:
            pids = obj.pids.all()
            if obj in pids:
                raise ValidationError("Нельзя связать человека с самим собой.")


class PersonAdmin(PersonAdminMixin, DraggableMPTTAdmin):
    pass


admin.site.register(Person, PersonAdmin)
