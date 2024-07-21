from datetime import timedelta

def calculate_work_hours_and_status(attendance_records):
    total_work_hours = timedelta()
    is_present = False

    for record in attendance_records:
        if record.login_time and record.logout_time:
            work_duration = record.logout_time - record.login_time
            total_work_hours += work_duration
            is_present = True
    
    total_hours = total_work_hours.total_seconds() / 3600  # Convert seconds to hours
    return total_hours, is_present


def calculate_work_hours_and_status_v1(attendance_records):
    total_work_hours = timedelta()
    is_present = False

    for record in attendance_records:
        if record.login_time and record.logout_time:
            work_duration = record.logout_time - record.login_time
            total_work_hours += work_duration
            is_present = True
    
    total_hours = total_work_hours.total_seconds() / 3600  # Convert seconds to hours
    return total_hours, is_present
