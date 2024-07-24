# Employee Attendance Management System

## Description
The Employee Attendance Management System is designed to track employees' attendance, including entry and exit times, working hours, and location status. The system provides APIs for managing employee records and attendance.

## Features
- Employee management (create, retrieve, update, delete)
- Attendance logging (check-in and check-out)
- Attendance reporting
- Working hours and status tracking

## Prerequisites
- Python 3.6+
- Django 3.2+
- SQLite 

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/employee-attendance-system.git
cd employee_management
```

### Step 2: Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Run the Development Server
```bash
python manage.py runserver
```
