from django.http import Http404
from .models import Annoucement
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AnnoucementSerializer


class AnnouncementView(APIView):
    def get(self, request):
        obj = Annoucement.objects.all()
        serializer = AnnoucementSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = AnnoucementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AnnouncementDetailView(APIView):
    def get_object(self, pk):
        try:
            return Annoucement.objects.get(pk=pk)
        except Annoucement.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        announcement = self.get_object(pk)
        serializer = AnnoucementSerializer(announcement)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        announcement = self.get_object(pk)
        serializer = AnnoucementSerializer(announcement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

