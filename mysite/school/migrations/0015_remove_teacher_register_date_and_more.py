# Generated by Django 4.1.4 on 2022-12-30 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0014_remove_student_student_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='register_date',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='teacher_name',
        ),
    ]
