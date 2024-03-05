from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Person
from .serializers import PersonSerializer


class TreeView(APIView):
    def get(self, request):
        root_nodes = Person.objects.filter(parent__isnull=True)
        max_descendants_node = None
        max_descendants_count = -1
        for node in root_nodes:
            descendants_count = node.get_descendant_count()
            if descendants_count > max_descendants_count:
                max_descendants_count = descendants_count
                max_descendants_node = node
        if max_descendants_node:
            serialized_tree = self.serialize_tree(max_descendants_node)
            return Response(serialized_tree, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Древо не найдено'}, status=status.HTTP_404_NOT_FOUND)

    def serialize_tree(self, node):
        serialized_data = PersonSerializer(node).data
        serialized_data['children'] = [self.serialize_tree(child) for child in node.get_children()]
        return serialized_data
