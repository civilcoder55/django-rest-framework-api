from django.urls import path

from . import views

app_name = 'departments'

urlpatterns = [
    path('', views.DepartmentListCreateAPIView.as_view(),
         name='department-list'),
    path('<pk>', views.DepartmentDetailsAPIView.as_view(),
         name='department-details'),
]
