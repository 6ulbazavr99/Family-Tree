from rest_framework import serializers
from tree.models import Person


class PersonSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('id', 'name', 'level', 'image', 'children', )

    def get_children(self, obj):
        if obj.subfamilies.exists():
            return PersonSerializer(obj.subfamilies.all(), many=True).data
        return []
