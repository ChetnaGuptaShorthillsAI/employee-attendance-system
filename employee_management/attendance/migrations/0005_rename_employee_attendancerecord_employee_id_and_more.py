# Generated by Django 5.0.7 on 2024-07-21 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_alter_attendancerecord_login_work_location_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendancerecord',
            old_name='employee',
            new_name='employee_id',
        ),
        migrations.RenameField(
            model_name='employeeworkingdetails',
            old_name='employee',
            new_name='employee_id',
        ),
    ]