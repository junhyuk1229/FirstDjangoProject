# Generated by Django 4.1.4 on 2022-12-17 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_alter_student_advisor_teacher_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='advisor_teacher',
        ),
        migrations.AddField(
            model_name='teacher',
            name='advising_student',
            field=models.ForeignKey(default=None, help_text='Teacher that advises the student', on_delete=django.db.models.deletion.CASCADE, to='school.student'),
            preserve_default=False,
        ),
    ]
