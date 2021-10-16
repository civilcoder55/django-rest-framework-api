from rest_framework.generics import ListCreateAPIView,\
    RetrieveUpdateDestroyAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from .models import Department
from .serializers import DepartmentSerializer


class DepartmentListCreateAPIView(ListCreateAPIView):
    """API view to retrieve list of departments or create new"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


class DepartmentDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update or delete department"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
