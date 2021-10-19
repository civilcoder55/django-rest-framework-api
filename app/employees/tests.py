from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from .models import Employee
from departments.models import Department

from .serializers import EmployeeDetailsSerializer

import tempfile
import os

from PIL import Image

EMPLOYEES_URL = reverse('employees:employee-list')


def detail_url(employee_id):
    """Return employee detail URL"""
    return reverse('employees:employee-details', args=[employee_id])


def sample_department(name='TEST', description='TEST DEPARTMENT'):
    """Create and return a sample department"""
    return Department.objects.create(name=name, description=description)


def sample_employee(first_name, last_name, email,
                    salary, hired_at, department, is_manager):
    """Create and return a sample employee"""
    return Employee.objects.create(first_name=first_name, last_name=last_name,
                                   email=email, salary=salary,
                                   hired_at=hired_at,
                                   department=department,
                                   is_manager=is_manager)


class PublicEmployeesApiTests(TestCase):
    """Test the publicly available employees API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving employees"""
        res = self.client.get(EMPLOYEES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEmployeesApiTests(TestCase):
    """Test the authorized user employees API"""

    def setUp(self):
        self.normal_user = get_user_model().objects.create_user(
            'test_normal_user',
            'password123'
        )
        self.super_user = get_user_model().objects.create_superuser(
            'test_super_user',
            'password123'
        )
        self.normal_client = APIClient()
        self.super_client = APIClient()
        self.super_client.force_authenticate(self.super_user)
        self.normal_client.force_authenticate(self.normal_user)

    def test_superuser_required(self):
        """Test that superuser is required for retrieving employees"""

        res = self.normal_client.get(EMPLOYEES_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_employees(self):
        """Test retrieving employees"""
        department = sample_department('IT', 'IT DEPARTMENT')
        sample_employee('John', 'Smith', 'john@test.com',
                        7500.00, timezone.now(), department, False)

        sample_employee('John', 'Doe', 'johndoe@test.com',
                        17500.00, timezone.now(), department, True)

        res = self.super_client.get(EMPLOYEES_URL)

        employees = Employee.objects.all()
        serializer = EmployeeDetailsSerializer(employees, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['last_name'], 'Smith')
        self.assertEqual(res.data[0]['is_manager'], False)
        self.assertEqual(res.data[1]['department'], 'IT')
        self.assertEqual(res.data[1]['is_manager'], True)

    def test_create_employee_successful(self):
        """Test creating a new employee"""
        department = sample_department('IT', 'IT DEPARTMENT')
        payload = {'first_name': 'Test', 'last_name': 'Name',
                   'email': 'test@email.com',
                   'salary': 7500.0, 'hired_at': timezone.now(),
                   'department': department.id,
                   'is_manager': False}
        self.super_client.post(EMPLOYEES_URL, payload)

        exists = Employee.objects.filter(
            email=payload['email']
        ).exists()
        self.assertTrue(exists)

    def test_employee_required_fields(self):
        """Test employee some fields are required"""
        payload = {'first_name': 'Test', 'last_name': 'Name',
                   'email': 'test@email.com',
                   'salary': '', 'hired_at': timezone.now(),
                   'department': '',
                   'is_manager': False}
        res = self.super_client.post(EMPLOYEES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('salary', res.data)
        self.assertIn('department', res.data)

    def test_employee_details_retrieve(self):
        """Test employee details can be retrieved"""
        department = sample_department('IT', 'IT DEPARTMENT')
        employee = sample_employee('John', 'Simth', 'john@test.com',
                                   7500.0, timezone.now(), department, False)

        url = detail_url(employee.id)
        res = self.super_client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], employee.email)
        self.assertEqual(res.data['department'], department.name)
        self.assertEqual(float(res.data['salary']), employee.salary)
        self.assertEqual(res.data['is_manager'], employee.is_manager)

    def test_employee_details_patched(self):
        """Test employee details can be patched"""
        department = sample_department('IT', 'IT DEPARTMENT')
        employee = sample_employee('John', 'Simth', 'john@test.com',
                                   7500.0, timezone.now(), department, False)

        url = detail_url(employee.id)
        payload = {'salary': 5000.0}
        res = self.super_client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        employee.refresh_from_db()

        self.assertEqual(employee.salary, payload['salary'])

    def test_employee_details_updated(self):
        """Test employee details can be updated"""
        department = sample_department('IT', 'IT DEPARTMENT')
        employee = sample_employee('John', 'Simth', 'john@test.com',
                                   7500.0, timezone.now(), department, False)

        url = detail_url(employee.id)
        payload = {'first_name': 'Test', 'last_name': 'Name',
                   'email': 'test@email.com',
                   'salary': 8000.0, 'hired_at': timezone.now(),
                   'department': department.id,
                   'is_manager': True}

        res = self.super_client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        employee.refresh_from_db()

        self.assertEqual(employee.salary, payload['salary'])
        self.assertEqual(employee.is_manager, payload['is_manager'])
        self.assertEqual(employee.department.id, payload['department'])

    def test_employee_details_deleted(self):
        """Test employee details can be deleted"""
        department = sample_department('IT', 'IT DEPARTMENT')
        employee = sample_employee('John', 'Simth', 'john@test.com',
                                   7500.0, timezone.now(), department, False)

        url = detail_url(employee.id)
        res = self.super_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = Employee.objects.filter(id=employee.id).exists()

        self.assertFalse(exists)

    def test_employee_details_invalid(self):
        """Test employee invalid pk can't be retrieved"""

        url = detail_url('1')
        res = self.super_client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class EmployeePictureUploadTests(TestCase):

    def setUp(self):
        self.super_user = get_user_model().objects.create_superuser(
            'test_super_user',
            'password123'
        )
        self.super_client = APIClient()
        self.super_client.force_authenticate(self.super_user)
        department = sample_department('IT', 'IT DEPARTMENT')
        self.employee = sample_employee('John', 'Simth', 'john@test.com',
                                        7500.0, timezone.now(),
                                        department, False)

    def tearDown(self):
        self.employee.picture.delete()

    def test_upload_picture_to_employee(self):
        """Test uploading a picture to employee"""
        url = detail_url(self.employee.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as temp:
            img = Image.new('RGB', (10, 10))
            img.save(temp, format='JPEG')
            temp.seek(0)
            res = self.super_client.patch(
                url, {'picture': temp}, format='multipart')

        self.employee.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('picture', res.data)
        self.assertTrue(os.path.exists(self.employee.picture.path))

    def test_upload_picture_bad_request(self):
        """Test uploading an invalid picture"""
        url = detail_url(self.employee.id)
        res = self.super_client.patch(
            url, {'picture': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
