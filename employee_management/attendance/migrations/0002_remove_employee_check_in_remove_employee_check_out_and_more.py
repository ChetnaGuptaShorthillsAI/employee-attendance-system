# Generated by Django 5.0.7 on 2024-07-21 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='check_in',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='check_out',
        ),
        migrations.AddField(
            model_name='employee',
            name='work_shift',
            field=models.CharField(choices=[('Morning', 'Morning'), ('Night', 'Night')], default='Morning', max_length=10),
            preserve_default=False,
        ),
    ]
