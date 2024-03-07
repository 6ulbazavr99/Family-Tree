# serializers.py
from rest_framework import serializers
from tree.models import Person
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PersonSerializer(serializers.ModelSerializer):
    relationships = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('id', 'name', 'generation', 'image', 'relationships', 'gender', 'mid', 'fid')

    def get_relationships(self, obj):
        relationships = []

        for child in obj.subfamilies.all():
            relationship = {
                'id': child.id,
                'pids': [obj.id],
                'name': child.name,
                'img': self.get_image(child),
                'gender': child.gender,
                'mid': obj.id,
                'fid': obj.parent.id if obj.parent else None,
            }

            relationships.append(relationship)

            relationships.extend(self.get_relationships(child))

        return relationships

    def get_image(self, obj):
        return f"http://127.0.0.1:8000{obj.image.url}"
