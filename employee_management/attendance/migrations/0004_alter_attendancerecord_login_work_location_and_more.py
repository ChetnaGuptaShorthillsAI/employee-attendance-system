# Generated by Django 5.0.7 on 2024-07-21 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_alter_attendancerecord_login_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancerecord',
            name='login_work_location',
            field=models.CharField(choices=[('Noida', 'Noida'), ('Gurugram', 'Gurugram'), ('Hybrid', 'Hybrid')], max_length=50),
        ),
        migrations.AlterField(
            model_name='attendancerecord',
            name='logout_work_location',
            field=models.CharField(choices=[('Noida', 'Noida'), ('Gurugram', 'Gurugram'), ('Hybrid', 'Hybrid')], max_length=50),
        ),
    ]