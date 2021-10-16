from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee objects"""

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class EmployeeDetailsSerializer(EmployeeSerializer):
    """Serializer for Employee Details objects"""
    department = serializers.StringRelatedField()
