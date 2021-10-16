from rest_framework import authentication, permissions
from rest_framework.generics import RetrieveUpdateAPIView,CreateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import UserSerializer


# class CreateUserView(generics.CreateAPIView):
#     """Create a new user in the system"""
#     serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserDetailsAPIView(RetrieveUpdateAPIView):
    """API view to retrieve, update authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user

