from datetime import datetime
from django.http import Http404
from .models import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import InventorySerializer, InventoryTypeSerializer


class InventoryView(APIView):
    def get(self, request, format=None):
        inventory = Inventory.objects.all()
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class InventoryDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        inventory = self.get_object(pk)
        serializer = InventorySerializer(inventory)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        staff = self.get_object(pk)
        serializer = InventorySerializer(staff, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InventoryCountView(APIView):
    def get(self, request, format=None):
        count = Inventory.objects.count()
        return Response({"count": count})
    
"""Inventory Type"""

class InventoryTypeView(APIView):
    def get(self, request, format=None):
        type = InventoryType.objects.all()
        serializer = InventoryTypeSerializer(type, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = InventoryTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class InventoryTypeDetailView(APIView):
    def get_object(self, pk):
        try:
            return InventoryType.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        type = self.get_object(pk)
        serializer = InventoryTypeSerializer(type)
        return Response(serializer.data)