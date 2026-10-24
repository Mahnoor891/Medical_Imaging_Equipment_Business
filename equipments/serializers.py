from rest_framework import serializers
from .models import Equipment
from .models import Category
# Built to convert basic instances into json

class EquipmentSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Equipment
        fields = '__all__'