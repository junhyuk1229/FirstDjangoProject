# Generated by Django 4.1.4 on 2022-12-17 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_teacher_advised_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='advised_student',
            field=models.IntegerField(),
        ),
    ]
