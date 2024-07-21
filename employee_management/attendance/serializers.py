from rest_framework import serializers
from .models import Employee,AttendanceRecord,EmployeeWorkingDetails

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name', 'employee_id', 'email', 'work_shift', 'is_active', 'created_at', 'updated_at']


class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = ['employee_id', 'login_work_location', 'login_time']

class CheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = ['employee_id', 'logout_work_location', 'logout_time']

class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = ['employee_id', 'login_time', 'logout_time', 'login_work_location', 'logout_work_location']

class EmployeeWorkingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeWorkingDetails
        fields = ['employee_id', 'date', 'location', 'working_hrs', 'is_present']
