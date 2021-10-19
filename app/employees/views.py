from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from .models import Employee
from .serializers import EmployeeSerializer, EmployeeDetailsSerializer


class EmployeeListCreateAPIView(ListCreateAPIView):
    """API view to retrieve list of employees or create new"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.request.method == 'GET':
            return EmployeeDetailsSerializer

        return EmployeeSerializer


class EmployeeDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update or delete employee"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.request.method == 'GET':
            return EmployeeDetailsSerializer

        return EmployeeSerializer
