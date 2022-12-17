# Generated by Django 4.1.4 on 2022-12-17 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_remove_student_advisor_teacher_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='advising_student',
        ),
        migrations.AddField(
            model_name='student',
            name='advisor_teacher',
            field=models.ForeignKey(default=None, help_text='Teacher that advises the student', on_delete=django.db.models.deletion.CASCADE, to='school.teacher'),
            preserve_default=False,
        ),
    ]
