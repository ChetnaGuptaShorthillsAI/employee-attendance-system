# Generated by Django 5.0.7 on 2024-07-21 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0007_rename_is_present_employeeworkingdetails_is_present_first_half_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeworkingdetails',
            name='location',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]