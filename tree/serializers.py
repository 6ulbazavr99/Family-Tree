from rest_framework import serializers
from tree.models import Person


class TreeSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('id', 'pids', 'mid', 'fid', 'name', 'img', 'gender')

    def get_img(self, obj):
        if obj.img and obj.img.url:
            return f"http://127.0.0.1:8000{obj.img.url}"
        return None
