from rest_framework import generics
from rest_framework.response import Response
from tree.models import Person
from tree.serializers import PersonSerializer


class PersonView(generics.ListAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data)
