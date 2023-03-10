# Generated by Django 4.1.4 on 2023-02-08 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0014_classstudentrelation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_user',
            field=models.ForeignKey(help_text='Student user', on_delete=django.db.models.deletion.CASCADE, to='school.schooluser', unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_user',
            field=models.ForeignKey(help_text='Teacher user', on_delete=django.db.models.deletion.CASCADE, to='school.schooluser', unique=True),
        ),
    ]
