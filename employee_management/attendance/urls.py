from django.urls import path
from .views import create_employee,get_employee,delete_inactive_employee,update_employee,log_employee_check_in_v1,log_employee_check_out_v2,get_employee_attendance,get_employee_working_hours_and_status

urlpatterns = [
    path('create_employee/', create_employee, name='create_employee'),
    path('get_employee/<str:employee_id>/', get_employee, name='get_employee'),
    path('delete_inactive_employee/<str:employee_id>/', delete_inactive_employee, name='delete_inactive_employee'),
    path('update_employee/<str:employee_id>/', update_employee, name='update_employee'),
    path('log_employee_check_in/<str:employee_id>/', log_employee_check_in_v1, name='log_employee_check_in'),
    path('log_employee_check_out/<str:employee_id>/', log_employee_check_out_v2, name='log_employee_check_out'),
    path('get_employee_attendance/<str:employee_id>/', get_employee_attendance, name='get_employee_attendance'),
    path('employee/<str:employee_id>/working-hours/<str:date>/',get_employee_working_hours_and_status, name='get_employee_working_hours_and_status'),

]
