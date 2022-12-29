import datetime
from django.db import models
from django.utils import timezone


class Teacher(models.Model):
    teacher_name = models.CharField(max_length=100, help_text="Teachers full name. First name first")
    register_date = models.DateTimeField('date_registered', default=timezone.now, help_text="Registered date to school")
    
    def __str__(self):
        return f"name: {self.teacher_name}\nregistered date: {self.register_date}"


class Student(models.Model):
    student_name = models.CharField(max_length=100, help_text="Students full name. First name first")
    register_date = models.DateTimeField('date_registered', default=timezone.now, help_text="Registered date to school")
    advisor_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, help_text="Teacher that advises the student", null=True)

    def __str__(self):
        return f"Name: {self.student_name}\nRegistered date: {self.register_date}\nAdvisor: {self.advisor_teacher.teacher_name}"


