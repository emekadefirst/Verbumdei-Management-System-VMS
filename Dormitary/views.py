from .models import Hostel, Dorm
from .serializers import HostelSerializer, DormSerializer, GetDormSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q


class HostelView(APIView):
    def get(self, request, format=None):
        hostels = Hostel.objects.all()
        serializer = HostelSerializer(hostels, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = HostelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HostelDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Hostel.objects.get(pk=pk)
        except Hostel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        room = self.get_object(pk)
        serializer = HostelSerializer(room)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        room = self.get_object(pk)
        serializer = HostelSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DormCountView(APIView):
    def get(self, request, format=None):
        count = Dorm.objects.count()
        return Response({"count": count})


class DormAPIView(APIView):
    def post(self, request):
        serializer = DormSerializer(data=request.data)
        if serializer.is_valid():
            dorm = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllDorm(APIView):
    def get(self, request, format=None):
        dorms = Dorm.objects.all()
        serializer = GetDormSerializer(dorms, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class DormDetail(APIView):

    def get_object(self, pk):
        try:
            return Dorm.objects.get(pk=pk)
        except Dorm.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dorm = self.get_object(pk)
        serializer = GetDormSerializer(dorm)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        room = self.get_object(pk)
        serializer = DormSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
