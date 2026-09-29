from rest_framework import viewsets
from .models import Shipment
from .serializers import ShipmentSerializer


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all().order_by('-shipment_date')
    serializer_class = ShipmentSerializer