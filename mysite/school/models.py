from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class Teacher(models.Model):
    teacher_user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Teacher user", null=True)

    def __str__(self):
        return f"Username: {self.teacher_user.username}"


class Student(models.Model):
    student_user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Student user", null=True)
    advisor_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, help_text="Teacher that advises the student", null=True)

    def __str__(self):
        return f"Username: {self.student_user.username}"


class Announcement(models.Model):
    anno_title = models.CharField(max_length=100)
    anno_content = models.TextField()
    anno_date = models.DateTimeField(default=timezone.now)
    auther_name = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Title: {self.anno_title}"

    def get_absolute_url(self):
        return reverse('school:anno_detail', kwargs={'pk': self.pk})