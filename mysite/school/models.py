from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import User
from . import validators as val


class SchoolUser(models.Model):
    class TypeTeacherStudent(models.TextChoices):
        STUDENT = 'S', ("Student")
        TEACHER = 'T', ("Teacher")
        ADMIN = 'A', ("Admin")
        UNDETERMINED = 'U', ("Undetermined")

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
        help_text="Type of user(Teacher, Student, Admin, Undetermined)",
    )

    def __str__(self):
        return f"\nPrimary Key: {self.pk}\nUser Type: {self.type_user}\nUsername: {self.site_user.username}\n"
    
    def get_absolute_url(self):
        return reverse('school:register_general')


class Teacher(models.Model):
    teacher_user = models.ForeignKey(
        SchoolUser,
        on_delete=models.CASCADE,
        null=False,
        help_text="Teacher user",
    )

    def __str__(self):
        return f"\nPrimery Key: {self.pk}\nUsername: {self.teacher_user.site_user.username}\n"
    
    def clean(self):
        if self.teacher_user.type_user != 'T':
            raise ValidationError(
                ('%(value)s is not a teacher(Value: %(type_user)s)'),
                params={'value': self.teacher_user.site_user.username, 'type_user': self.teacher_user.type_user},
            )


class Student(models.Model):
    student_user = models.ForeignKey(
        SchoolUser,
        on_delete=models.CASCADE,
        null=False,
        validators=[val.check_student_schooluser_valid],
        help_text="Student user",
    )

    advisor_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Teacher that advises the student",
    )

    def __str__(self):
        return f"\nPrimery Key: {self.pk}\nUsername: {self.student_user.site_user.username}\n"
    
    def clean(self):
        if self.student_user.type_user != 'S':
            raise ValidationError(
                ('%(value)s is not a student(Value: %(type_user)s)'),
                params={'value': self.student_user.site_user.username, 'type_user': self.student_user.type_user},
            )


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
        SchoolUser,
        on_delete=models.CASCADE,
        help_text="Name of auther",
    )

    def __str__(self):
        return f"\nPrimary Key: {self.pk}\nTitle: {self.anno_title}\nCreation Date: {self.anno_date}\nAuthor Username: {self.auther_name.site_user.username}\n"

    def get_absolute_url(self):
        return reverse('school:anno_detail', kwargs={'pk': self.pk})
    
    def clean(self):
        if self.auther_name.type_user not in ['A', 'T']:
            raise ValidationError(
                ('%(value)s is not a admin or teacher(Value: %(type_user)s)'),
                params={'value': self.auther_name.site_user.username, 'type_user': self.auther_name.type_user},
            )


class Subject(models.Model):
    subject_name = models.CharField(
        max_length=100,
        help_text="Name of subject",
    )

    def __str__(self):
        return f"\nPrimary Key: {self.pk}\nSubject: {self.subject_name}"


class SchoolClass(models.Model):
    class_subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        help_text="Subject the class is based on",
    )

    class_time = models.IntegerField(
        validators=[val.check_schoolclass_semester_valid],
        help_text="Year + semester of the subject",
    )

    assigned_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        help_text="Teacher teaching class",
    )

    def __str__(self):
        return f"\nPrimery Key: {self.pk}\nClass Time: {self.class_time}\nAssigned Teacher: {self.assigned_teacher.teacher_user.site_user.username}\n"


class ClassStudentRelation(models.Model):
    class_relate = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        help_text="Connected class to student",
    )

    student_relate = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        help_text="Connected student to class",
    )

    def __str__(self):
        return f"\nPrimery Key: {self.pk}\nClass Subject: {self.class_relate.class_subject}\nClass Time: {self.class_relate.class_time}\nAssigned Teacher: {self.class_relate.assigned_teacher.teacher_user.site_user.username}\nStudent: {self.student_relate.student_user.site_user.username}\n"
