from decimal import Decimal
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from equipments.models import Equipment
from hospitals.models import Hospital


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),                              # enquiry sent, waiting for admin
        ('Rejected', 'Rejected'),                            # admin rejected it
        ('Awaiting Confirmation', 'Awaiting Confirmation'),  # admin accepted, hospital reviewing
        ('Confirmed', 'Confirmed'),                          # hospital placed the order
        ('Cancelled', 'Cancelled'),                          # hospital cancelled
    ]

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    order_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True, default='')
    shipping_address = models.TextField()

    estimated_timeline = models.CharField(max_length=100, blank=True, default='')
    admin_note = models.TextField(blank=True, default='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_status = self.status      # remember the status to detect changes

    @property
    def total(self):
        return sum((item.line_total for item in self.items.all()), Decimal('0'))

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            staff = get_user_model().objects.filter(is_staff=True)
            notify(staff, f"New enquiry #{self.id} from {self.customer_name}.", self)
        elif self.status != self._old_status:
            self._notify_status_change()

        self._old_status = self.status

    def _notify_status_change(self):
        staff = get_user_model().objects.filter(is_staff=True)
        hospital_user = self.hospital.user if self.hospital else None

        if self.status == 'Awaiting Confirmation' and hospital_user:
            timeline = self.estimated_timeline or 'to be confirmed'
            notify(
                [hospital_user],
                f"Order #{self.id} was accepted. Estimated timeline: {timeline}. "
                f"Please review it and place your order.",
                self,
            )
        elif self.status == 'Rejected' and hospital_user:
            message = f"Order #{self.id} was rejected."
            if self.admin_note:
                message += f" Reason: {self.admin_note}"
            notify([hospital_user], message, self)
        elif self.status == 'Confirmed':
            notify(staff, f"{self.customer_name} placed order #{self.id}.", self)
        elif self.status == 'Cancelled':
            notify(staff, f"{self.customer_name} cancelled order #{self.id}.", self)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    @property
    def line_total(self):
        return (self.price or Decimal('0')) * self.quantity

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.equipment.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.equipment.name} - Order #{self.order.id}"


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.message[:40]}"


def notify(users, message, order=None):
    Notification.objects.bulk_create(
        [Notification(user=user, order=order, message=message) for user in users]
    )