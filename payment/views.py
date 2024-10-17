import os
from datetime import datetime, timedelta
from django.db.models import Sum
from django.http import Http404
from .models import Payment, PaymentType, PhysicalPayment
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from student.models import Student
from .serializers import PaymentSerializers, PaymentTypeSerializer, GetPhysicalPaymentSerializer, MakePhysicalPaymentSerializer


secret_key = os.environ.get("SECRET_KEY")


class PaymentTypeView(APIView):
    def get(self, request, format=None):
        type = PaymentType.objects.all()
        serializer = PaymentTypeSerializer(type, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = PaymentTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllPaymentView(APIView):
    def get(self, request, format=None):
        payment = Payment.objects.all()
        serializer = PaymentSerializers(payment, many=True)
        return Response(serializer.data)


class PaymentDetailView(APIView):
    def get_object(self, pk):
        try:
            return Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        payment = self.get_object(pk)
        serializer = PaymentSerializers(payment)
        return Response(serializer.data)

class PhysicalView(APIView):
    def get(self, request):
        obj = PhysicalPayment.objects.all()
        serializer = GetPhysicalPaymentSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = MakePhysicalPaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhysicalPaymentView(APIView):
    def get_object(self, pk):
        try:
            return PhysicalPayment.objects.get(pk=pk)
        except PhysicalPayment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        payment = self.get_object(pk)
        serializer = GetPhysicalPaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        payment = self.get_object(pk)
        serializer = MakePhysicalPaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TotalPayment(APIView):
    def get(self, request, format=None):
        total_physical_payment = (
            PhysicalPayment.objects.aggregate(total=Sum("amount_paid"))["total"] or 0
        )
        total_payment = (
            Payment.objects.aggregate(total=Sum("payment_type__amount"))["total"] or 0
        )

        total = total_physical_payment + total_payment
        return Response({"total_payment": total})





class TotalTuitionForMonth(APIView):
    def get(self, request, format=None):
        current_time = datetime.now()
        first_day_current_month = current_time.replace(day=1)
        last_day_previous_month = first_day_current_month - timedelta(days=1)
        first_day_previous_month = last_day_previous_month.replace(day=1)

        current_month_physical_payments = (
            PhysicalPayment.objects.filter(
                time__year=current_time.year, time__month=current_time.month
            ).aggregate(total_amount=Sum("amount_paid"))["total_amount"]
            or 0
        )
        current_month_online_payments = (
            Payment.objects.filter(
                created_at__year=current_time.year, created_at__month=current_time.month
            ).aggregate(total_amount=Sum("payment_type__amount"))["total_amount"]
            or 0
        )

        # Sum of physical and online payments for the current month
        total_current_month_payments = (
            current_month_physical_payments + current_month_online_payments
        )

        # Get total physical payments for the previous month
        previous_month_physical_payments = (
            PhysicalPayment.objects.filter(
                time__year=last_day_previous_month.year,
                time__month=last_day_previous_month.month,
            ).aggregate(total_amount=Sum("amount_paid"))["total_amount"]
            or 0
        )

        # Get total online payments for the previous month
        previous_month_online_payments = (
            Payment.objects.filter(
                created_at__year=last_day_previous_month.year,
                created_at__month=last_day_previous_month.month,
            ).aggregate(total_amount=Sum("payment_type__amount"))["total_amount"]
            or 0
        )

        # Sum of physical and online payments for the previous month
        total_previous_month_payments = (
            previous_month_physical_payments + previous_month_online_payments
        )

        # Calculate the percentage change
        if total_previous_month_payments > 0:
            percentage_change = (
                (total_current_month_payments - total_previous_month_payments)
                / total_previous_month_payments
            ) * 100
        else:
            percentage_change = 0

        # Format the response data
        response_data = {
            "total_tuition_for_current_month": f"₦{total_current_month_payments:,.2f}",
            "percentage_change": f"{percentage_change:+.2f}%",
        }

        return Response(response_data)


class StudentPaymentHistory(APIView):
    def get(self, request, registration_id):
        try:
            student = Student.objects.get(registration_id=registration_id)
        except Student.DoesNotExist:
            return Response({"detail": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        payments = PhysicalPayment.objects.filter(student=student)
        
        if payments.exists():
            serializer = GetPhysicalPaymentSerializer(payments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": "No payments found for the student"}, status=status.HTTP_404_NOT_FOUND)
