# Generated by Django 4.1.4 on 2022-12-22 10:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0010_remove_teacher_advised_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='advisor_teacher',
            field=models.ForeignKey(help_text='Teacher that advises the student', null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.teacher'),
        ),
        migrations.AlterField(
            model_name='student',
            name='register_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Registered date to school', verbose_name='date_registered'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='register_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Registered date to school', verbose_name='date_registered'),
        ),
    ]