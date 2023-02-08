# Generated by Django 4.1.4 on 2023-02-08 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0009_alter_schoolclass_class_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='auther_name',
            field=models.ForeignKey(help_text='Name of auther', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
