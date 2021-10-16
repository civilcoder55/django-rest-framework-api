from django.db import models
from django.db.models.fields import BooleanField
from departments.models import Department
from .utils import gen_pic_file_path

# Create your models here.


class Employee(models.Model):
    """employee model"""
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    salary = models.DecimalField(max_digits=7, decimal_places=2)
    picture = models.ImageField(null=True, upload_to=gen_pic_file_path)
    hired_at = models.DateTimeField(null=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    is_manager = BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
