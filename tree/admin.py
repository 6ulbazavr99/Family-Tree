from django.contrib import admin
from django.contrib.auth.models import User, Group
from mptt.admin import MPTTModelAdmin
from .models import Person


class PersonAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent', 'birthdate')
    list_filter = ('parent', 'birthdate')
    search_fields = ('name',)


admin.site.register(Person, PersonAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
