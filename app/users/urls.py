from django.urls import path

from . import views

urlpatterns = [
    path('token/', views.CreateTokenView.as_view(), name='token-create'),
    path('me/', views.UserDetailsAPIView.as_view(), name='user-details'),
]
