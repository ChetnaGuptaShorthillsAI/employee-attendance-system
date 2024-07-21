from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from .models import Employee, AttendanceRecord, EmployeeWorkingDetails

class EmployeeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Clean up existing data to avoid conflicts
        Employee.objects.filter(employee_id='E123').delete()

        self.employee_data = {
            "name": "XYZ",
            "employee_id": "E123",
            "email": "xyz@shorthillstech.com",
            "work_shift": "Morning"
        }
        self.updated_employee_data = {
            'name': 'abc'
        }
        url = "http://127.0.0.1:8000/api"
        self.create_employee_url = f'{url}/create_employee/'
        self.get_employee_url = f'{url}/get_employee/E123/'
        self.delete_inactive_employee_url = f'{url}/delete_inactive_employee/E123/'
        self.update_employee_url = f'{url}/update_employee/E123/'
        self.log_employee_check_in_url = f'{url}/log_employee_check_in/E123/'
        self.log_employee_check_out_url = f'{url}/log_employee_check_out/E123/'
        self.get_employee_attendance_url = f'{url}/get_employee_attendance/E123/'
        self.get_employee_working_hours_and_status_v1_url = f'{url}/employee/E123/working-hours/2024-07-21/'

        # Create initial employee
        self.client.post(self.create_employee_url, self.employee_data, format='json')

    def test_get_employee(self):
        response = self.client.get(self.get_employee_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employee_id'], self.employee_data['employee_id'])

    def test_update_employee(self):
        response = self.client.patch(self.update_employee_url, self.updated_employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.updated_employee_data['name'])

    def test_delete_inactive_employee(self):
        # Mark employee as inactive
        Employee.objects.filter(employee_id='E123').update(is_active=False)
        response = self.client.delete(self.delete_inactive_employee_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_log_employee_check_in(self):
        now = timezone.now()
        response = self.client.post(self.log_employee_check_in_url, {
            'login_work_location': 'Noida'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AttendanceRecord.objects.count(), 1)
        self.assertEqual(AttendanceRecord.objects.first().login_work_location, 'Noida')

    def test_log_employee_check_out(self):
        # First log in
        self.client.post(self.log_employee_check_in_url, {'login_work_location': 'Noida'}, format='json')
        now = timezone.now()
        response = self.client.post(self.log_employee_check_out_url, {
            'logout_work_location': 'Noida'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(AttendanceRecord.objects.count(), 1)
        self.assertIsNotNone(AttendanceRecord.objects.first().logout_time)

    def test_get_employee_attendance(self):
        # Log in and out to create attendance record
        self.client.post(self.log_employee_check_in_url, {'login_work_location': 'Noida'}, format='json')
        self.client.post(self.log_employee_check_out_url, {'logout_work_location': 'Noida'}, format='json')
        response = self.client.get(self.get_employee_attendance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_employee_working_hours_and_status_v1(self):
        # Log in and out to create attendance record and working details
        self.client.post(self.log_employee_check_in_url, {'login_work_location': 'Noida'}, format='json')
        self.client.post(self.log_employee_check_out_url, {'logout_work_location': 'Noida'}, format='json')
        response = self.client.get(self.get_employee_working_hours_and_status_v1_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employee_id'], 'E123')
        self.assertEqual(response.data['location'], 'Noida')

    def tearDown(self):
        Employee.objects.all().delete()
        AttendanceRecord.objects.all().delete()
        EmployeeWorkingDetails.objects.all().delete()
