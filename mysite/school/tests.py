from datetime import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from users.models import User
from school.models import SchoolUser, Teacher, Student, Announcement, Subject, SchoolClass, ClassStudentRelation
from django.urls import reverse


class CheckCreateModelSchoolUser(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Jun')
        temp_user.set_password('Kim')
        temp_user.save()
        SchoolUser.objects.create(site_user=temp_user, type_user='A')

    def test_schooluser_created_check(self):
        SchoolUser.objects.get(pk=1)

    def test_schooluser_only_one_created_check(self):
        with self.assertRaises(IndexError):
            SchoolUser.objects.all()[1]

    def test_schooluser_instance_check(self):
        temp_schooluser = SchoolUser.objects.get(pk=1)
        self.assertIsInstance(temp_schooluser, SchoolUser)

    def test_schooluser_string_return_check(self):
        temp_schooluser = SchoolUser.objects.get(pk=1)
        self.assertEqual(temp_schooluser.__str__(), f"\nPrimary Key: {temp_schooluser.pk}\nUser Type: {temp_schooluser.type_user}\nUsername: {temp_schooluser.site_user.username}\n")


class CheckCreateModelTeacher(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Jun')
        temp_user.set_password('Kim')
        temp_user.save()
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='T')
        Teacher.objects.create(teacher_user=temp_schooluser)

    def test_teacher_created_check(self):
        Teacher.objects.get(pk=1)

    def test_teacher_only_one_created_check(self):
        with self.assertRaises(IndexError):
            Teacher.objects.all()[1]

    def test_teacher_wrong_type_user_check(self):
        temp_user = User.objects.create(username='Kim')
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='A')
        temp_teacher = Teacher.objects.create(teacher_user=temp_schooluser)
        with self.assertRaises(ValidationError):
            temp_teacher.clean()

    def test_teacher_instance_check(self):
        temp_teacher = Teacher.objects.get(pk=1)
        self.assertIsInstance(temp_teacher, Teacher)

    def test_teacher_string_return_check(self):
        temp_teacher = Teacher.objects.get(pk=1)
        self.assertEqual(temp_teacher.__str__(), f"\nPrimery Key: {temp_teacher.pk}\nUsername: {temp_teacher.teacher_user.site_user.username}\n")


class CheckCreateModelStudent(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Jun')
        temp_user.set_password('Kim')
        temp_user.save()
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='S')
        Student.objects.create(student_user=temp_schooluser)

    def test_student_created_check(self):
        Student.objects.get(pk=1)

    def test_student_only_one_created_check(self):
        with self.assertRaises(IndexError):
            Student.objects.all()[1]

    def test_student_wrong_type_user_check(self):
        temp_user = User.objects.create(username='Kim')
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='A')
        temp_student = Student.objects.create(student_user=temp_schooluser)
        with self.assertRaises(ValidationError):
            temp_student.clean()

    def test_student_instance_check(self):
        temp_student = Student.objects.get(pk=1)
        self.assertIsInstance(temp_student, Student)

    def test_student_string_return_check(self):
        temp_student = Student.objects.get(pk=1)
        self.assertEqual(temp_student.__str__(), f"\nPrimery Key: {temp_student.pk}\nUsername: {temp_student.student_user.site_user.username}\n")


class CheckCreateModelAnnouncement(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Jun')
        temp_user.set_password('Kim')
        temp_user.save()
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='A')
        Announcement.objects.create(anno_title='title', anno_content='content', anno_date=datetime.now(), auther_name=temp_schooluser)

    def test_announcement_created_check(self):
        Announcement.objects.get(pk=1)

    def test_announcement_only_one_created_check(self):
        with self.assertRaises(IndexError):
            Announcement.objects.all()[1]

    def test_announcement_wrong_type_user_check(self):
        temp_user = User.objects.create(username='Kim')
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='S')
        temp_announcement = Announcement.objects.create(anno_title='title', anno_content='content', anno_date=datetime.now(), auther_name=temp_schooluser)
        with self.assertRaises(ValidationError):
            temp_announcement.clean()

    def test_announcement_instance_check(self):
        temp_announcement = Announcement.objects.get(pk=1)
        self.assertIsInstance(temp_announcement, Announcement)

    def test_announcement_string_return_check(self):
        temp_announcement = Announcement.objects.get(pk=1)
        self.assertEqual(temp_announcement.__str__(), f"\nPrimary Key: {temp_announcement.pk}\nTitle: {temp_announcement.anno_title}\nCreation Date: {temp_announcement.anno_date}\nAuthor Username: {temp_announcement.auther_name.site_user.username}\n")


class CheckCreateModelSubject(TestCase):
    @classmethod
    def setUp(self):
        Subject.objects.create(subject_name='English')

    def test_subject_created_check(self):
        Subject.objects.get(pk=1)

    def test_subject_only_one_created_check(self):
        with self.assertRaises(IndexError):
            Subject.objects.all()[1]

    def test_subject_instance_check(self):
        temp_subject = Subject.objects.get(pk=1)
        self.assertIsInstance(temp_subject, Subject)

    def test_subject_string_return_check(self):
        temp_subject = Subject.objects.get(pk=1)
        self.assertEqual(temp_subject.__str__(), f"\nPrimary Key: {temp_subject.pk}\nSubject: {temp_subject.subject_name}")


class CheckCreateModelSchoolClass(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Jun')
        temp_user.set_password('Kim')
        temp_user.save()
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='T')
        temp_subject = Subject.objects.create(subject_name='English')
        temp_teacher = Teacher.objects.create(teacher_user=temp_schooluser)
        SchoolClass.objects.create(class_subject=temp_subject, class_time=20122, assigned_teacher=temp_teacher)

    def test_schoolclass_created_check(self):
        SchoolClass.objects.get(pk=1)

    def test_schoolclass_only_one_created_check(self):
        with self.assertRaises(IndexError):
            SchoolClass.objects.all()[1]

    def test_schoolclass_create_wrong_classtime(self):
        temp_subject = Subject.objects.get(pk=1)
        temp_teacher = Teacher.objects.get(pk=1)
        temp_schoolclass = SchoolClass.objects.create(class_subject=temp_subject, class_time=201201, assigned_teacher=temp_teacher)
        with self.assertRaises(ValidationError):
            temp_schoolclass.full_clean()
        temp_schoolclass = SchoolClass.objects.create(class_subject=temp_subject, class_time=400001, assigned_teacher=temp_teacher)
        with self.assertRaises(ValidationError):
            temp_schoolclass.full_clean()
        temp_schoolclass = SchoolClass.objects.create(class_subject=temp_subject, class_time=100001, assigned_teacher=temp_teacher)
        with self.assertRaises(ValidationError):
            temp_schoolclass.full_clean()

    def test_schoolclass_instance_check(self):
        temp_schoolclass = SchoolClass.objects.get(pk=1)
        self.assertIsInstance(temp_schoolclass, SchoolClass)

    def test_schoolclass_string_return_check(self):
        temp_schoolclass = SchoolClass.objects.get(pk=1)
        self.assertEqual(temp_schoolclass.__str__(), f"\nPrimery Key: {temp_schoolclass.pk}\nClass Time: {temp_schoolclass.class_time}\nAssigned Teacher: {temp_schoolclass.assigned_teacher.teacher_user.site_user.username}\n")


class CheckCreateModelClassStudentRelation(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Jun')
        temp_user.set_password('Kim')
        temp_user.save()
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='T')
        temp_subject = Subject.objects.create(subject_name='English')
        temp_teacher = Teacher.objects.create(teacher_user=temp_schooluser)
        temp_schoolclass = SchoolClass.objects.create(class_subject=temp_subject, class_time=20122, assigned_teacher=temp_teacher)
        temp_user = User.objects.create(username='John')
        temp_user.set_password('Kim')
        temp_user.save()
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='S')
        temp_student = Student.objects.create(student_user=temp_schooluser)
        ClassStudentRelation.objects.create(class_relate=temp_schoolclass, student_relate=temp_student)
    
    def test_class_student_relation_created_check(self):
        ClassStudentRelation.objects.get(pk=1)

    def test_class_student_relation_only_one_created_check(self):
        with self.assertRaises(IndexError):
            ClassStudentRelation.objects.all()[1]

    def test_class_student_relation_instance_check(self):
        temp_relation = ClassStudentRelation.objects.get(pk=1)
        self.assertIsInstance(temp_relation, ClassStudentRelation)

    def test_class_student_relation_string_return_check(self):
        temp_relation = ClassStudentRelation.objects.get(pk=1)
        self.assertEqual(temp_relation.__str__(), f"\nPrimery Key: {temp_relation.pk}\nClass Subject: {temp_relation.class_relate.class_subject}\nClass Time: {temp_relation.class_relate.class_time}\nAssigned Teacher: {temp_relation.class_relate.assigned_teacher.teacher_user.site_user.username}\nStudent: {temp_relation.student_relate.student_user.site_user.username}\n")



