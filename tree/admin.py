from django.contrib import admin
from django.core.mail import EmailMessage
from mptt.admin import DraggableMPTTAdmin
from .models import Person
from django.core.exceptions import ValidationError
from django import forms
from import_export.admin import ImportExportModelAdmin
from .resources import PersonResource
from import_export.admin import ExportActionMixin
from import_export.formats.base_formats import XLSX
from mptt.exceptions import InvalidMove


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
            depth = obj.level
            arrow = '--> ' * depth
            return f"{arrow} {obj.name}"
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
        try:
            super().save_model(request, obj, form, change)
        except InvalidMove as e:
            self.message_user(request, f"Ошибка: {e}", level='ERROR')

    def save_related(self, request, form, formsets, change):
        try:
            super().save_related(request, form, formsets, change)
        except InvalidMove as e:
            self.message_user(request, f"Ошибка: {e}", level='ERROR')


class CustomExportActionMixin(ExportActionMixin):
    def get_export_resource_class(self):
        return PersonResource

    def export_resource(self, queryset):
        resource = self.get_export_resource_class()()
        dataset = resource.export(queryset)
        return dataset.xlsx


def export_and_send_email(modeladmin, request, queryset):
    exporter = CustomExportActionMixin()
    try:
        exported_data = exporter.export_resource(queryset)
        admin_email = request.user.email
        subject = 'Экспортированные данные'
        message = 'Здесь находятся экспортированные данные.'
        email_from = admin_email
        recipient_list = [admin_email]
        email = EmailMessage(subject, message, email_from, recipient_list)
        email.attach('Persons.xlsx', exported_data, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        email.send()
    except Exception as e:
        modeladmin.message_user(request, f"Ошибка при экспорте и отправке по почте: {e}", level='ERROR')


export_and_send_email.short_description = "Экспорт и отправка по почте"


class PersonAdmin(PersonAdminMixin, DraggableMPTTAdmin, ImportExportModelAdmin):
    resource_class = PersonResource
    actions = [export_and_send_email]

    def get_export_formats(self):
        return [XLSX]

    def get_import_formats(self):
        return [XLSX]


admin.site.register(Person, PersonAdmin)
admin.site.site_header = "Семейное Древо"
