from rest_framework import serializers

from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department objects"""

    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
