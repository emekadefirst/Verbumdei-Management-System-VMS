from .models.term import Term
from .serializers import TermSerializer
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response



class TermView(APIView):
    def get(self, request, format=None):
        term = Term.objects.all()
        serializer = TermSerializer(term, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TermSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TermDetailView(APIView):
    def get_object(self, pk):
        try:
            return Term.objects.get(pk=pk)
        except Term.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        term = self.get_object(pk)
        serializer = TermSerializer(term)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        term = self.get_object(pk)
        serializer = TermSerializer(term, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


