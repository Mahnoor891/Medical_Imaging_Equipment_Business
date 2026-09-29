from rest_framework import serializers
from .models import Equipment
# Built to convert basic instances into json

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'