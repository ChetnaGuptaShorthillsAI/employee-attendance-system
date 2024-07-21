from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee,AttendanceRecord,EmployeeWorkingDetails
from .serializers import EmployeeSerializer,CheckInSerializer,CheckOutSerializer,AttendanceRecordSerializer,EmployeeWorkingDetailsSerializer
from django.utils import timezone
from .utils import calculate_work_hours_and_status_v2


@api_view(['POST'])
def create_employee(request):
    if request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_employee(request, employee_id):
    try:
        employee = Employee.objects.get(employee_id=employee_id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
def delete_inactive_employee(request, employee_id):
    try:
        employee = Employee.objects.get(employee_id=employee_id)
        if not employee.is_active:
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Employee is still active and cannot be deleted"}, status=status.HTTP_400_BAD_REQUEST)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    
@api_view(['PATCH'])
def update_employee(request, employee_id):
    try:
        employee = Employee.objects.get(employee_id=employee_id)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = EmployeeSerializer(employee, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['GET'])
def get_employee_attendance(request, employee_id):
    try:
        employee = Employee.objects.get(employee_id=employee_id)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    attendance_records = AttendanceRecord.objects.filter(employee_id=employee_id)
    serializer = AttendanceRecordSerializer(attendance_records, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_employee_working_hours_and_status(request, employee_id, date):
    try:
        work_details = EmployeeWorkingDetails.objects.get(employee_id=employee_id, date=date)
    except EmployeeWorkingDetails.DoesNotExist:
        return Response({"error": "Work details not found for the given date"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = EmployeeWorkingDetailsSerializer(work_details)
    return Response(serializer.data, status=status.HTTP_200_OK)


    logout_work_location = request.data.get('logout_work_location')
    
    try:
        employee = Employee.objects.get(employee_id=employee_id)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
    
    now = timezone.now()
    current_date = now.date()

    try:
        attendance_record = AttendanceRecord.objects.filter(
            employee_id=employee, 
            login_time__date=current_date
        ).latest('login_time')
    except AttendanceRecord.DoesNotExist:
        return Response({"error": "No check-in record found for today."}, status=status.HTTP_404_NOT_FOUND)
    
    if attendance_record.logout_time:
        return Response({"error": "Employee has already checked out for today."}, status=status.HTTP_400_BAD_REQUEST)
    
    attendance_record.logout_work_location = logout_work_location
    attendance_record.logout_time = now
    
    serializer = CheckOutSerializer(attendance_record, data={
        'logout_work_location': logout_work_location,
        'logout_time': now
    }, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        
        # Calculate work hours and presence
        attendance_records = AttendanceRecord.objects.filter(
            employee_id=employee, 
            login_time__date=attendance_record.login_time.date()
        )
        total_hours, is_present_first_half, is_present_second_half = calculate_work_hours_and_status_v2(
            attendance_records,
            employee.work_shift
        )        
        # Save work details
        EmployeeWorkingDetails.objects.update_or_create(
            employee_id=employee,
            date=attendance_record.login_time.date(),
            defaults={
                'location': logout_work_location,
                'working_hrs': total_hours,
                'is_present_first_half': is_present_first_half,
                'is_present_second_half': is_present_second_half
            }
        )
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def log_employee_check_in_v2(request, employee_id):
    login_work_location = request.data.get('login_work_location')
    
    try:
        employee = Employee.objects.get(employee_id=employee_id)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
    
    now = timezone.now()
    current_date = now.date()
    
    # Check if employee already checked in today for their shift
    existing_check_in = AttendanceRecord.objects.filter(
        employee_id=employee, 
        login_time__date=current_date, 
        login_work_location=login_work_location
    ).exists()

    if existing_check_in:
        return Response({"error": "Employee has already checked in for today."}, status=status.HTTP_400_BAD_REQUEST)
    
    data = {
        'employee_id': employee_id,
        'login_work_location': login_work_location,
        'login_time': now
    }
    
    serializer = CheckInSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        
        # Save initial details in EmployeeWorkingDetails
        EmployeeWorkingDetails.objects.update_or_create(
            employee_id=employee,
            date=current_date,
            defaults={
                'location': login_work_location,
                'working_hrs': 4,
                'is_present_first_half': True,
                'is_present_second_half': False
            }
        )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def log_employee_check_out_v3(request, employee_id):
    logout_work_location = request.data.get('logout_work_location')
    
    try:
        employee = Employee.objects.get(employee_id=employee_id)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
    
    now = timezone.now()
    current_date = now.date()

    try:
        attendance_record = AttendanceRecord.objects.filter(
            employee_id=employee, 
            login_time__date=current_date
        ).latest('login_time')
    except AttendanceRecord.DoesNotExist:
        return Response({"error": "No check-in record found for today."}, status=status.HTTP_404_NOT_FOUND)
    
    if attendance_record.logout_time:
        return Response({"error": "Employee has already checked out for today."}, status=status.HTTP_400_BAD_REQUEST)
    
    attendance_record.logout_work_location = logout_work_location
    attendance_record.logout_time = now
    
    serializer = CheckOutSerializer(attendance_record, data={
        'logout_work_location': logout_work_location,
        'logout_time': now
    }, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        
        # Calculate work hours and presence
        attendance_records = AttendanceRecord.objects.filter(
            employee_id=employee, 
            login_time__date=attendance_record.login_time.date()
        )
        total_hours, is_present_first_half, is_present_second_half = calculate_work_hours_and_status_v2(
            attendance_records,
            employee.work_shift
        )
        
        # Save work details
        EmployeeWorkingDetails.objects.update_or_create(
            employee_id=employee,
            date=attendance_record.login_time.date(),
            defaults={
                'location': logout_work_location,
                'working_hrs': total_hours,
                'is_present_first_half': is_present_first_half,
                'is_present_second_half': is_present_second_half
            }
        )
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
