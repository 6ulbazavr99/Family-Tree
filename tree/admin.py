from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.db import transaction
from django.core.exceptions import ValidationError
from django import forms
from .models import Person


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


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    form = PersonForm
    list_display = ('indented_title', 'name', 'title', 'parent', 'fid', 'mid', 'get_pids', 'birthdate', 'gender')
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
        ('Персональные данные', {'fields': ('name', 'title', 'birthdate', 'gender')}),
        ('Семейная связь', {'fields': ('parent', 'fid', 'mid', 'pids')}),
        ('Изображение', {'fields': ('img',), 'classes': ('collapse',)}),
    )

    readonly_fields = ('indented_title',)
    verbose_name = 'Человек'
    verbose_name_plural = 'Люди'

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if 'pids' in form.changed_data:
            pids = obj.pids.all()
            if obj in pids:
                raise ValidationError("Нельзя связать человека с самим собой.")


admin.site.site_header = "Семейное древо"
admin.site.site_title = "Администрирование Семейного древа"
admin.site.unregister(Group)
admin.site.unregister(User)
