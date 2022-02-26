from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from main.models import Patient, User
from .serializers import PatientSerializer, UserSerializer
from .permissions import IsReceptionist, IsDoctor


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    permission_classes = [IsReceptionist| IsDoctor]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = []