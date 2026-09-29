from rest_framework import serializers
from .models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            'id',
            'order',
            'shipment_date',
            'shipping_address',
            'tracking_number',
            'status',
        ]