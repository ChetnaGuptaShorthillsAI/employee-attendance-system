Employee Attendance Management System
Description
The Employee Attendance Management System is designed to track employees' attendance, including entry and exit times, working hours, and location status. The system provides APIs for managing employee records and attendance.

Features
Employee management (create, retrieve, update, delete)
Attendance logging (check-in and check-out)
Attendance reporting
Working hours and status tracking
Prerequisites
Python 3.6+
Django 3.2+
SQLite (default for development)
Installation
Step 1: Clone the Repository
bash
Copy code
git clone https://github.com/yourusername/employee_attendance_management.git
cd employee_attendance_management
Step 2: Set Up Virtual Environment
Create and activate a virtual environment:

bash
Copy code
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
Step 3: Install Dependencies
Install the necessary packages using pip:

bash
Copy code
pip install -r requirements.txt
Step 4: Configure the Database
Apply database migrations:

bash
Copy code
python manage.py migrate
Step 5: Run the Server
Start the Django development server:

bash
Copy code
python manage.py runserver
Access the application at http://127.0.0.1:8000/

API Endpoints
Employee Management
Create Employee: POST /api/create_employee/
Get Employee: GET /api/get_employee/<employee_id>/
Update Employee: PATCH /api/update_employee/<employee_id>/
Delete Inactive Employee: DELETE /api/delete_inactive_employee/<employee_id>/
Attendance Management
Log Check-In: POST /api/log_employee_check_in/<employee_id>/
Log Check-Out: POST /api/log_employee_check_out/<employee_id>/
Get Employee Attendance: GET /api/get_employee_attendance/<employee_id>/
Get Working Hours and Status: GET /api/employee/<employee_id>/working-hours/<date>/
Running Tests
To run the unit tests, use the following command:

bash
Copy code
python manage.py test
