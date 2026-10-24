from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Hospital
from .serializers import HospitalSerializer, HospitalProfileSerializer


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAdminUser]


# The logged-in client reads and edits only their own hospital
class MyHospitalView(generics.RetrieveUpdateAPIView):
    serializer_class = HospitalProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_object(self):
        try:
            return self.request.user.hospital
        except Hospital.DoesNotExist:
            raise NotFound('Your account is not linked to a hospital.')