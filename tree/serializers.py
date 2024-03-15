from rest_framework import serializers
from tree.models import Person


class TreeSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('id', 'pids', 'mid', 'fid', 'name', 'img', 'gender', 'title')

    def get_img(self, obj):
        if obj.img and obj.img.url:
            return obj.img.url
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['mid'] is None:
            del data['mid']
        if data['fid'] is None:
            del data['fid']
        if data['title'] is None:
            del data['title']
        return data
