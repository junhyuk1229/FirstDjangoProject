# Generated by Django 4.1.4 on 2023-02-05 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_alter_schooluser_type_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='advisor_teacher',
            field=models.OneToOneField(help_text='Teacher that advises the student', null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.teacher'),
        ),
    ]
