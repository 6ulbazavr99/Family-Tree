from import_export import resources, fields
from .models import Person


class PersonResource(resources.ModelResource):
    parent_id = fields.Field(column_name='parent_id', attribute='parent_id')

    class Meta:
        model = Person
        fields = ('id', 'name', 'title', 'img', 'birthdate', 'gender', 'parent_id', 'fid', 'mid', 'pids')

    def dehydrate_parent_id(self, person):
        return person.parent_id if person.parent else None
