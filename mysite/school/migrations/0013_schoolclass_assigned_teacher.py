# Generated by Django 4.1.4 on 2023-02-08 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0012_alter_announcement_auther_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolclass',
            name='assigned_teacher',
            field=models.ForeignKey(default=0, help_text='Teacher teaching class', on_delete=django.db.models.deletion.CASCADE, to='school.teacher'),
            preserve_default=False,
        ),
    ]
