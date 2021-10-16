from django.urls import path

from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.EmployeeListCreateAPIView.as_view(),
         name='employee-list'),
    path('<pk>', views.EmployeeDetailsAPIView.as_view(),
         name='employee-details'),
]
