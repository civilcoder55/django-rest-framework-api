from django.contrib import admin
from departments.models import Department
from employees.models import Employee
# Register your models here.

admin.site.register(Department)
admin.site.register(Employee)
