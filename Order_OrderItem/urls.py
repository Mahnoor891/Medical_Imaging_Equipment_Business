from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, NotificationViewSet

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='order')
router.register('notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]