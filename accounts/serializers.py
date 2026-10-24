from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers

from hospitals.models import Hospital


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    hospital_name = serializers.CharField(max_length=200, write_only=True)
    branch = serializers.CharField(
        max_length=200, required=False, allow_blank=True, write_only=True
    )
    phone = serializers.CharField(max_length=20, write_only=True)
    address = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password',
            'hospital_name', 'branch', 'phone', 'address',
        ]
        extra_kwargs = {'email': {'required': True, 'allow_blank': False}}

    def validate_password(self, value):
        validate_password(value)
        return value

    @transaction.atomic
    def create(self, validated_data):
        hospital_data = {
            'name': validated_data.pop('hospital_name'),
            'branch': validated_data.pop('branch', '') or 'Main',
            'phone': validated_data.pop('phone'),
            'address': validated_data.pop('address'),
        }
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        Hospital.objects.create(
            user=user, email=validated_data['email'], **hospital_data
        )
        return user