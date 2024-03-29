from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Person
from .serializers import TreeSerializer


class TreeView(APIView):
    def get(self, request):
        all_nodes = Person.objects.all()
        serialized_nodes = [self.serialize_node(node) for node in all_nodes]

        if serialized_nodes:
            return Response(serialized_nodes, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Древо не найдено'}, status=status.HTTP_404_NOT_FOUND)

    def serialize_node(self, node):
        return TreeSerializer(node).data
