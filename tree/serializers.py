from rest_framework import serializers
from tree.models import Person


class PersonSerializer(serializers.ModelSerializer):
    childs = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('id', 'name', 'level', 'image', 'childs')

    def get_childs(self, obj):
        if obj.subfamilies.exists():
            return PersonSerializer(obj.subfamilies.all(), many=True).data
        return []
