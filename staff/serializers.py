from rest_framework import serializers
from .models import Staff, AccountInfo, Payroll

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff  
        fields = '__all__'

    def create(self, validated_data):
        staff = Staff.objects.create(**validated_data)
        return staff

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class AccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountInfo
        fields = '__all__'
        
    def create(self, validated_data):
        payroll = AccountInfo.objects.create(**validated_data)
        return payroll

    def update(self, instance, validated_data):
        payroll = super().update(instance, validated_data) 
        return payroll

class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = '__all__'

    def create(self, validated_data):
        payroll = Payroll.objects.create(**validated_data)
        payroll.calculate_net_pay()  
        payroll.generate_transaction_reference()  
        return payroll
    
    def update(self, instance, validated_data):
        payroll = super().update(instance, validated_data)
        payroll.calculate_net_pay()  
        return payroll
