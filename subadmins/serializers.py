from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Sub_Admin

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']



class SubAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Sub_Admin
        fields = ['id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        sub_admin = Sub_Admin.objects.create(user=user, **validated_data)
        return sub_admin

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        # Update the user fields
        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()

        # Update the Sub_Admin fields
        instance.save()
        return instance
