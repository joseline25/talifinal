# Generated by Django 4.1.3 on 2022-12-06 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='instructorprogram',
            old_name='coursefulltime',
            new_name='course',
        ),
        migrations.RemoveField(
            model_name='instructorprogram',
            name='date',
        ),
        migrations.RemoveField(
            model_name='instructorprogram',
            name='day',
        ),
        migrations.RemoveField(
            model_name='instructorprogram',
            name='hours',
        ),
        migrations.RemoveField(
            model_name='instructorprogram',
            name='moment',
        ),
        migrations.RemoveField(
            model_name='instructorprogram',
            name='week',
        ),
        migrations.RemoveField(
            model_name='instructorprogram',
            name='week_number',
        ),
    ]