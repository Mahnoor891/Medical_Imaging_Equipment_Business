from django.contrib import admin, messages
from .models import Order, OrderItem, Notification


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.action(description='Accept selected enquiries')
def accept_orders(modeladmin, request, queryset):
    accepted = 0
    skipped = 0
    for order in queryset:
        if order.status != 'Pending':
            skipped += 1
            continue
        if not order.estimated_timeline:
            messages.warning(
                request,
                f"Order #{order.id}: fill in the estimated timeline before accepting."
            )
            continue
        order.status = 'Awaiting Confirmation'
        order.save()
        accepted += 1
    if accepted:
        messages.success(request, f"{accepted} enquiry(ies) accepted.")
    if skipped:
        messages.warning(request, f"{skipped} order(s) skipped: only Pending enquiries can be accepted.")


@admin.action(description='Reject selected enquiries')
def reject_orders(modeladmin, request, queryset):
    rejected = 0
    skipped = 0
    for order in queryset:
        if order.status != 'Pending':
            skipped += 1
            continue
        order.status = 'Rejected'
        order.save()
        rejected += 1
    if rejected:
        messages.success(request, f"{rejected} enquiry(ies) rejected.")
    if skipped:
        messages.warning(request, f"{skipped} order(s) skipped: only Pending enquiries can be rejected.")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'hospital', 'customer_name', 'status', 'total', 'estimated_timeline', 'order_date')
    list_filter = ('status',)
    search_fields = ('customer_name', 'customer_email')
    readonly_fields = ('order_date',)
    inlines = [OrderItemInline]
    actions = [accept_orders, reject_orders]

    def changelist_view(self, request, extra_context=None):
        pending = Order.objects.filter(status='Pending').count()
        if pending:
            messages.info(request, f"{pending} pending enquiry(ies) waiting for your review.")
        return super().changelist_view(request, extra_context)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'equipment', 'quantity', 'price')


@admin.action(description='Mark selected notifications as read')
def mark_read(modeladmin, request, queryset):
    queryset.update(is_read=True)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'is_read', 'created_at')
    list_filter = ('is_read',)
    actions = [mark_read]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(user=request.user)