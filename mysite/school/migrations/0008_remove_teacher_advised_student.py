# Generated by Django 4.1.4 on 2022-12-17 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_alter_teacher_advised_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='advised_student',
        ),
    ]
