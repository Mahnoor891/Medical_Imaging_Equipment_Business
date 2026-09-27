from django.shortcuts import render

from rest_framework import viewsets
from .models import Equipment
from .serializers import EquipmentSerializer
from .permissions import IsAdminOrReadOnly


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAdminOrReadOnly]