from django.db import models

class Employee(models.Model):
    WORK_SHIFT_CHOICES = [
        ('Morning', 'Morning'),
        ('Night', 'Night'),
    ]

    name = models.CharField(max_length=255, null=False)
    employee_id = models.CharField(max_length=255, unique=True, primary_key=True, null=False)
    email = models.EmailField(unique=True, null=False)
    work_shift = models.CharField(max_length=10, choices=WORK_SHIFT_CHOICES, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AttendanceRecord(models.Model):
    WORK_LOCATIONS = [
        ('Noida', 'Noida'),
        ('Gurugram', 'Gurugram'),
        ('Home', 'Home'),
    ]

    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    login_work_location = models.CharField(max_length=50, choices=WORK_LOCATIONS, null=True, blank=True)
    logout_work_location = models.CharField(max_length=50, choices=WORK_LOCATIONS, null=True, blank=True)

    def __str__(self):
        return f"AttendanceRecord({self.employee_id.name})"

class EmployeeWorkingDetails(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    location = models.CharField(max_length=50, null=False)
    working_hrs = models.IntegerField()
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"EmployeeWorkingDetails({self.employee.name} - {self.date})"
