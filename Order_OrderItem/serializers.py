from rest_framework import serializers
from .models import Order, OrderItem, Notification


class OrderItemSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    line_total = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'equipment', 'equipment_name', 'quantity', 'price', 'line_total']
        read_only_fields = ['price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'hospital', 'customer_name', 'customer_email', 'customer_phone',
            'shipping_address', 'order_date', 'status', 'estimated_timeline',
            'admin_note', 'items', 'total',
        ]
        read_only_fields = [
            'hospital', 'customer_name', 'customer_email', 'customer_phone',
            'shipping_address', 'status', 'estimated_timeline', 'admin_note',
        ]

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError('Add at least one equipment item.')
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'order', 'is_read', 'created_at']
        read_only_fields = ['message', 'order', 'created_at']