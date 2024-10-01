from .serializers import CommuteSerializer, GetCommuteSerializer
from .bus_serializer import BusSerializer, GetBusSerializer
from .models import Bus, Commute
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class BusView(APIView):
    def get(self, request, format=None): 
        bus = Bus.objects.all()
        serializer = GetBusSerializer(bus, many=True)
        return Response(
            serializer.data, status=status.HTTP_200_OK
        ) 

    def post(self, request, format=None):
        serializer = BusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusCount(APIView):
    def get(self, request, format=None):
        count = Bus.objects.count()
        return Response(
            {"count": count}, status=status.HTTP_200_OK
        ) 


class BusDetailView(APIView):
    def get_object(self, pk):
        try:
            return Bus.objects.get(pk=pk)
        except Bus.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        bus = self.get_object(pk)
        serializer = BusSerializer(bus)
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )

    def put(self, request, pk, format=None):
        bus = self.get_object(pk)
        serializer = BusSerializer(bus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommuteView(APIView):
    def get(self, request, format=None): 
        commute = Commute.objects.all() 
        serializer = GetCommuteSerializer(commute, many=True)
        return Response(
            serializer.data, status=status.HTTP_200_OK
        ) 

    def post(self, request, format=None):
        serializer = CommuteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommuteDetailView(APIView):
    def get_object(self, pk):
        try:
            return Commute.objects.get(pk=pk)
        except Commute.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        commute = self.get_object(pk) 
        serializer = GetCommuteSerializer(commute)
        return Response(
            serializer.data, status=status.HTTP_200_OK
        ) 

    def put(self, request, pk, format=None):
        commute = self.get_object(pk) 
        serializer = CommuteSerializer(commute, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_202_ACCEPTED
            ) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
