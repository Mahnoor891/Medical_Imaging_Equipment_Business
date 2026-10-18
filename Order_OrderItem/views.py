from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hospitals.models import Hospital
from Invoice.models import Invoice
from Shipment.models import Shipment
from .models import Order, Notification
from .serializers import OrderSerializer, OrderItemSerializer, NotificationSerializer


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.all().order_by('-order_date')
        if user.is_staff:
            return orders
        # a hospital sees only its own orders; cancelled ones are hidden
        return orders.filter(hospital__user=user).exclude(status='Cancelled')

    # Hospital submits an enquiry
    def perform_create(self, serializer):
        try:
            hospital = self.request.user.hospital
        except Hospital.DoesNotExist:
            raise serializers.ValidationError('Your account is not linked to a hospital.')

        serializer.save(
            hospital=hospital,
            customer_name=str(hospital)[:150],
            customer_email=hospital.email,
            customer_phone=hospital.phone,
            shipping_address=hospital.address,
            status='Pending',
        )

    # Change quantity or remove one item (only after the admin accepted)
    @action(detail=True, methods=['get', 'patch', 'delete'], url_path=r'items/(?P<item_id>\d+)')
    def item(self, request, pk=None, item_id=None):

        order = self.get_object()
        item = get_object_or_404(order.items, pk=item_id)

        if request.method == 'GET':
            return Response(self.get_serializer(order).data)


       
        if order.status != 'Awaiting Confirmation':
            return Response(
                {'detail': 'Items can only be changed while the order is Awaiting Confirmation.'},
                status=400
            )

        if request.method == 'DELETE':
            item.delete()
            if not order.items.exists():
                order.status = 'Cancelled'      # nothing left, so the order is cancelled
                order.save()
        else:
            try:
                quantity = int(request.data.get('quantity'))
            except (TypeError, ValueError):
                return Response({'quantity': 'Enter a whole number.'}, status=400)
            if quantity < 1:
                return Response({'quantity': 'Quantity must be at least 1.'}, status=400)
            item.quantity = quantity
            item.save()

        return Response(self.get_serializer(order).data)
    # Hospital places the order -> invoice + shipment are created
    @action(detail=True, methods=['post'])
    def place(self, request, pk=None):
        order = self.get_object()

        if order.status != 'Awaiting Confirmation':
            return Response({'detail': 'Only accepted orders can be placed.'}, status=400)
        if not order.items.exists():
            return Response({'detail': 'This order has no items.'}, status=400)

        with transaction.atomic():
            order.status = 'Confirmed'
            order.save()
            Invoice.objects.get_or_create(
                order=order,
                defaults={'total_amount': order.total},
            )
            Shipment.objects.get_or_create(
                order=order,
                defaults={'shipping_address': order.shipping_address, 'status': 'Pending'},
            )

        return Response(self.get_serializer(order).data)

    # Hospital rejects / cancels
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()

        if order.status not in ('Pending', 'Awaiting Confirmation'):
            return Response({'detail': 'This order can no longer be cancelled.'}, status=400)

        order.status = 'Cancelled'
        order.save()
        return Response({'detail': 'Order cancelled.'})

    # Invoice page data
    @action(detail=True, methods=['get'])
    def invoice(self, request, pk=None):
        order = self.get_object()

        invoice = getattr(order, 'invoice', None)
        if invoice is None:
            return Response({'detail': 'No invoice yet. The order has not been placed.'}, status=404)

        shipment = getattr(order, 'shipment', None)

        return Response({
            'invoice_id': invoice.id,
            'invoice_date': invoice.invoice_date,
            'invoice_status': invoice.status,
            'order_id': order.id,
            'hospital': order.customer_name,
            'email': order.customer_email,
            'phone': order.customer_phone,
            'shipping_address': order.shipping_address,
            'items': OrderItemSerializer(order.items.all(), many=True).data,
            'total_amount': invoice.total_amount,
            'estimated_timeline': order.estimated_timeline,
            'shipment': {
                'status': shipment.status,
                'shipment_date': shipment.shipment_date,
                'expected_delivery_date': shipment.expected_delivery_date,
                'tracking_number': shipment.tracking_number,
            } if shipment else None,
        })

class NotificationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response(self.get_serializer(notification).data)

    @action(detail=False, methods=['post'], url_path='read-all')
    def read_all(self, request):
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'detail': 'All notifications marked as read.'})

    @action(detail=False, methods=['get'], url_path='unread-count')
    def unread_count(self, request):
        return Response({'unread': self.get_queryset().filter(is_read=False).count()})