# Generated by Django 4.1.4 on 2023-02-08 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0016_alter_teacher_teacher_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_user',
            field=models.OneToOneField(help_text='Student user', on_delete=django.db.models.deletion.CASCADE, to='school.schooluser'),
        ),
    ]