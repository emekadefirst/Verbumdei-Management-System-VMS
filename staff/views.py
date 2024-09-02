from django.http import Http404
from rest_framework import status
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Staff, AccountInfo, Payroll
from .serializers import StaffSerializer, AccountInfoSerializer, PayrollSerializer


class StaffListCreateAPIView(APIView):
    def get(self, request, format=None):
        staff = Staff.objects.all()
        serializer = StaffSerializer(
            staff, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Staff.objects.get(pk=pk)
        except Staff.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        staff = self.get_object(pk)
        serializer = StaffSerializer(staff)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        staff = self.get_object(pk)
        serializer = StaffSerializer(staff, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountCountView(APIView):
    def get(self, request, format=None):
        count = AccountInfo.objects.count()
        return Response({"count": count})


class AccountInfoListCreateAPIView(APIView):
    def get(self, request, format=None):
        account_info = AccountInfo.objects.all()
        serializer = AccountInfoSerializer(account_info, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AccountInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountInfoDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return AccountInfo.objects.get(pk=pk)
        except AccountInfo.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        account_info = self.get_object(pk)
        serializer = AccountInfoSerializer(account_info)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        account_info = self.get_object(pk)
        serializer = AccountInfoSerializer(account_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayrollListCreateAPIView(APIView):
    def get(self, request, format=None):
        payroll = Payroll.objects.all()
        serializer = PayrollSerializer(payroll, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PayrollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayrollDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Payroll.objects.get(pk=pk)
        except Payroll.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        payroll = self.get_object(pk)
        serializer = PayrollSerializer(payroll)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        payroll = self.get_object(pk)
        serializer = PayrollSerializer(payroll, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayrollExportAPIView(APIView):
    def get(self, request, pay_period, format=None):
        response = Payroll.export_to_csv(datetime.strptime(pay_period, "%Y-%m-%d"))
        return response


class StaffCountView(APIView):
    def get(self, request, format=None):
        count = Staff.objects.count()
        return Response({"count": count})


class StaffSearch(APIView):
    def post(self, request):
        search_query = request.data.get("query", "")
        if search_query:
            search_results = Staff.objects.filter(
                Q(name__icontains=search_query)
                | Q(staff_registration_id__icontains=search_query)
                | Q(first_name__icontains=search_query)
                | Q(other_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
            )

            search_results = search_results.order_by("staff_registration_id")
            serializer = StaffSerializer(search_results, many=True)
            print(f"Search results: {serializer.data}")
            return Response(serializer.data)
        else:
            return Response("Invalid search query", status=status.HTTP_400_BAD_REQUEST)
