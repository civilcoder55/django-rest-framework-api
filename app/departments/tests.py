from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .models import Department

from .serializers import DepartmentSerializer


DEPARTMENTS_URL = reverse('departments:department-list')


def detail_url(department_id):
    """Return department detail URL"""
    return reverse('departments:department-details', args=[department_id])


def sample_department(name='TEST', description='TEST DEPARTMENT'):
    """Create and return a sample department"""
    return Department.objects.create(name=name, description=description)


class PublicDepartmentsApiTests(TestCase):
    """Test the publicly available departments API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving departments"""
        res = self.client.get(DEPARTMENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDepartmentsApiTests(TestCase):
    """Test the authorized user departments API"""

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
        """Test that superuser is required for retrieving departments"""

        res = self.normal_client.get(DEPARTMENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_departments(self):
        """Test retrieving departments"""
        sample_department('IT', 'IT DEPARTMENT')
        sample_department('HR', 'HR DEPARTMENT')

        res = self.super_client.get(DEPARTMENTS_URL)

        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[1]['name'], 'HR')
        self.assertEqual(res.data[1]['description'], 'HR DEPARTMENT')

    def test_create_department_successful(self):
        """Test creating a new department"""
        payload = {'name': 'TEST', 'description': 'Test DEPARTMENT'}
        self.super_client.post(DEPARTMENTS_URL, payload)

        exists = Department.objects.filter(
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_department_name_description_required(self):
        """Test department name and description are required"""
        payload = {'name': '', 'description': ''}
        res = self.super_client.post(DEPARTMENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', res.data)
        self.assertIn('description', res.data)

    def test_department_details_retrieve(self):
        """Test department details can be retrieved"""
        department = sample_department('IT', 'IT DEPARTMENT')

        url = detail_url(department.id)
        res = self.super_client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], department.name)
        self.assertEqual(res.data['description'], department.description)

    def test_department_details_patched(self):
        """Test department details can be patched"""
        department = sample_department('IT', 'IT DEPARTMENT')

        url = detail_url(department.id)
        payload = {'description': 'IT DEPARTMENT for networking'}
        res = self.super_client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        department.refresh_from_db()

        self.assertEqual(department.description, payload['description'])

    def test_department_details_updated(self):
        """Test department details can be updated"""
        department = sample_department('IT', 'IT DEPARTMENT')

        url = detail_url(department.id)
        payload = {'name': 'NEW IT',
                   'description': 'IT DEPARTMENT for networking'}
        res = self.super_client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        department.refresh_from_db()

        self.assertEqual(department.name, payload['name'])
        self.assertEqual(department.description, payload['description'])

    def test_department_details_deleted(self):
        """Test department details can be deleted"""
        department = sample_department('IT', 'IT DEPARTMENT')

        url = detail_url(department.id)
        res = self.super_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = Department.objects.filter(id=department.id).exists()

        self.assertFalse(exists)

    def test_department_details_invalid(self):
        """Test department invalid pk can't be retrieved"""

        url = detail_url('1')
        res = self.super_client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
