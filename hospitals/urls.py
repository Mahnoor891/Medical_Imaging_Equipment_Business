from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HospitalViewSet, MyHospitalView

router = DefaultRouter()
router.register('hospitals', HospitalViewSet)

urlpatterns = [
    path('my-hospital/', MyHospitalView.as_view()),
    path('', include(router.urls)),
]