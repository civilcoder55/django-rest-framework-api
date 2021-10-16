from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication

from django.urls import path

schema_view = get_schema_view(
    openapi.Info(
        title="Employees Management API",
        default_version='v1',
        description="Employees Management API System",
    ),
    public=True,
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
]
