from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class SchoolUser(models.Model):
    class TypeTeacherStudent(models.TextChoices):
        STUDENT = 'S', ("Student")
        TEACHER = 'T', ("Teacher")

    site_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False,
        help_text="User of school website",
    )

    type_user = models.CharField(
        max_length=1,
        choices=TypeTeacherStudent.choices,
        default=TypeTeacherStudent.STUDENT,
        help_text="Type of user(Teacher, Student)",
    )

    def __str__(self):
        return f"\n\
            Primary Key: {self.pk}\n\
            Username: {self.site_user.username}\n\
            Type: {self.type_user}\n"


class Teacher(models.Model):
    teacher_user = models.ForeignKey(
        SchoolUser,
        on_delete=models.CASCADE,
        null=False,
        help_text="Teacher user",
    )

    def __str__(self):
        return f"\n\
            Primery Key: {self.pk}\n\
            Username: {self.teacher_user.site_user.username}\n"


class Student(models.Model):
    student_user = models.ForeignKey(
        SchoolUser,
        on_delete=models.CASCADE,
        null=False,
        help_text="Student user",
    )

    advisor_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Teacher that advises the student",
    )

    def __str__(self):
        return f"\n\
            Primery Key: {self.pk}\n\
            Username: {self.student_user.site_user.username}\n\
            Teacher Username: {self.advisor_teacher.teacher_user.site_user.username}\n"


class Announcement(models.Model):
    anno_title = models.CharField(
        max_length=100,
        help_text="Title of announcement",
    )

    anno_content = models.TextField(
        help_text="Content of announcement",
    )
    
    anno_date = models.DateTimeField(
        default=timezone.now,
        help_text="Date of creation",
    )

    auther_name = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Name of auther",
    )

    def __str__(self):
        return f"\n\
            Primary Key: {self.pk}\n\
            Title: {self.anno_title}\n\
            Creation Date: {self.anno_date}\n\
            Author Username: {self.auther_name.username}\n"

    def get_absolute_url(self):
        return reverse('school:anno_detail', kwargs={'pk': self.pk})