from datetime import datetime, time, timedelta

def calculate_work_hours_and_status_v2(attendance_records, shift):
    total_work_hours = timedelta()
    is_present_first_half = False
    is_present_second_half = False
    
    morning_start = time(10, 0)
    morning_end = time(18, 0)
    night_start = time(22, 0)
    night_end = time(6, 0)  # End time of the next day

    # Flag to determine if the logout time is missing
    missing_logout = False
    missing_login = False

    for record in attendance_records:
        if record.login_time and record.logout_time:
            work_duration = record.logout_time - record.login_time
            total_work_hours += work_duration

            # Determine if it's morning or night shift
            if shift == 'Morning':
                if record.login_time.time() <= morning_end and record.logout_time.time() >= morning_start:
                    is_present_first_half = True
                if record.login_time.time() <= morning_end and record.logout_time.time() >= morning_start:
                    is_present_second_half = True
            elif shift == 'Night':
                if (record.login_time.time() <= night_end or record.login_time.time() >= night_start) and \
                   (record.logout_time.time() <= night_end or record.logout_time.time() >= night_start):
                    is_present_first_half = True
                if (record.login_time.time() <= night_end or record.login_time.time() >= night_start) and \
                   (record.logout_time.time() <= night_end or record.logout_time.time() >= night_start):
                    is_present_second_half = True
    
    # Handle missing logout or login
    last_record = attendance_records.last()
    now = datetime.now().time()
    
    if shift == 'Morning':
        if last_record and not last_record.logout_time:
            if last_record.login_time.time() <= morning_end and now >= time(20, 0):
                is_present_first_half = True
                is_present_second_half = False
            elif last_record.login_time.time() > morning_end:
                is_present_first_half = False
                is_present_second_half = True
            else:
                is_present_first_half = False
                is_present_second_half = False

        if not last_record or not last_record.login_time:
            if now <= morning_end:
                is_present_first_half = False
                is_present_second_half = True
            else:
                is_present_first_half = False
                is_present_second_half = False

    elif shift == 'Night':
        if last_record and not last_record.logout_time:
            if last_record.login_time.time() <= night_end and now >= time(6, 0):
                is_present_first_half = True
                is_present_second_half = False
            elif last_record.login_time.time() > night_end:
                is_present_first_half = False
                is_present_second_half = True
            else:
                is_present_first_half = False
                is_present_second_half = False

        if not last_record or not last_record.login_time:
            if now <= night_end:
                is_present_first_half = False
                is_present_second_half = True
            else:
                is_present_first_half = False
                is_present_second_half = False

    total_hours = total_work_hours.total_seconds() / 3600  # Convert seconds to hours
    return total_hours, is_present_first_half, is_present_second_half
