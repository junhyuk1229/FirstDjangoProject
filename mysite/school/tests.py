from datetime import datetime
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase, Client
from users.models import User
from school.models import SchoolUser, Teacher, Student, Announcement, Subject, SchoolClass, ClassStudentRelation
from django.urls import reverse


class CheckSchoolModelSchoolUser(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Jun')
        temp_user.set_password('test123')
        temp_user.save()
        SchoolUser.objects.create(site_user=temp_user, type_user='A')

    def test_schooluser_created_check(self):
        SchoolUser.objects.get(pk=1)

    def test_schooluser_only_one_created_check(self):
        with self.assertRaises(IndexError):
            SchoolUser.objects.all()[1]

    def test_schooluser_same_user_error_check(self):
        temp_user = User.objects.get(pk=1)
        with self.assertRaises(IntegrityError):
            SchoolUser.objects.create(site_user=temp_user, type_user='U')


class CheckSchoolModelTeacher(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Jun')
        temp_user.set_password('test123')
        temp_user.save()
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='T')
        Teacher.objects.create(teacher_user=temp_schooluser)

    def test_teacher_created_check(self):
        Teacher.objects.get(pk=1)

    def test_teacher_only_one_created_check(self):
        with self.assertRaises(IndexError):
            Teacher.objects.all()[1]

    def test_teacher_same_schooluser_check(self):
        temp_schooluser = SchoolUser.objects.get(pk=1)
        with self.assertRaises(IntegrityError):
            Teacher.objects.create(teacher_user=temp_schooluser)

    def test_teacher_wrong_type_user_check(self):
        temp_user = User.objects.create(username='Kim')
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='A')
        temp_teacher = Teacher.objects.create(teacher_user=temp_schooluser)
        with self.assertRaises(ValidationError):
            temp_teacher.clean()


class CheckSchoolModelStudent(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Jun')
        temp_user.set_password('Kim')
        temp_user.save()
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='S')
        Student.objects.create(student_user=temp_schooluser)

    def test_student_created_check(self):
        Student.objects.get(pk=1)

    def test_student_only_one_check(self):
        with self.assertRaises(IndexError):
            Student.objects.all()[1]

    def test_student_same_schooluser_check(self):
        temp_schooluser = SchoolUser.objects.get(pk=1)
        with self.assertRaises(IntegrityError):
            Student.objects.create(student_user=temp_schooluser)

    def test_student_wrong_type_user_check(self):
        temp_user = User.objects.create(username='Kim')
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='A')
        temp_student = Student.objects.create(student_user=temp_schooluser)
        with self.assertRaises(ValidationError):
            temp_student.clean()


class CheckSchoolModelAnnouncement(TestCase):
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


class CheckSchoolModelSubject(TestCase):
    @classmethod
    def setUp(self):
        Subject.objects.create(subject_name='English')

    def test_subject_created_check(self):
        Subject.objects.get(pk=1)

    def test_subject_only_one_created_check(self):
        with self.assertRaises(IndexError):
            Subject.objects.all()[1]


class CheckSchoolModelSchoolClass(TestCase):
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

    def test_schoolclass_create_wrong_classtime_check(self):
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


class CheckSchoolModelClassStudentRelation(TestCase):
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


class CheckSchoolViewMain(TestCase):
    def test_school_main_page_status_check(self):
        temp_client = Client()
        temp_resp = temp_client.get("/school/")
        self.assertEqual(temp_resp.status_code, 200)

    def test_school_main_page_status_check_reverse(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('school:school_main'))
        self.assertEqual(temp_resp.status_code, 200)


class CheckSchoolViewTeacherGeneral(TestCase):
    def test_school_teacher_general_status_check(self):
        temp_client = Client()
        temp_resp = temp_client.get("/school/teacher")
        self.assertEqual(temp_resp.status_code, 200)

    def test_school_teacher_general_status_check_reverse(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('school:teacher_general'))
        self.assertEqual(temp_resp.status_code, 200)


class CheckSchoolViewTeacherDetail(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Jun')
        temp_user.set_password('test123')
        temp_user.save()
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='T')
        Teacher.objects.create(teacher_user=temp_schooluser)

    def test_school_teacher_detail_status_check_teacher_created(self):
        temp_client = Client()
        temp_resp = temp_client.get("/school/teacher/1")
        self.assertEqual(temp_resp.status_code, 200)

    def test_school_teacher_detail_status_check_teacher_not_created(self):
        temp_client = Client()
        temp_resp = temp_client.get("/school/teacher/2")
        self.assertEqual(temp_resp.status_code, 404)

    def test_school_teacher_detail_status_check_reverse(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('school:teacher_detail', kwargs={'pk':1}))
        self.assertEqual(temp_resp.status_code, 200)


class CheckSchoolViewStudentGeneral(TestCase):
    def test_school_student_general_status_check(self):
        temp_client = Client()
        temp_resp = temp_client.get("/school/student")
        self.assertEqual(temp_resp.status_code, 200)

    def test_school_student_general_status_check_reverse(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('school:student_general'))
        self.assertEqual(temp_resp.status_code, 200)


class CheckSchoolViewStudentDetail(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Jun')
        temp_user.set_password('test123')
        temp_user.save()
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='T')
        Student.objects.create(student_user=temp_schooluser)

    def test_school_student_detail_status_check_student_created(self):
        temp_client = Client()
        temp_resp = temp_client.get("/school/student/1")
        self.assertEqual(temp_resp.status_code, 200)

    def test_school_student_detail_status_check_student_not_created(self):
        temp_client = Client()
        temp_resp = temp_client.get("/school/student/2")
        self.assertEqual(temp_resp.status_code, 404)

    def test_school_student_detail_status_check_reverse(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('school:student_detail', kwargs={'pk':1}))
        self.assertEqual(temp_resp.status_code, 200)


class CheckSchoolViewAnnoGeneral(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Admin')
        temp_user.set_password('adm')
        temp_user.save()
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='A')
        
        Announcement.objects.create(anno_title='title', anno_content='content', anno_date=datetime.now(), auther_name=temp_schooluser)

        temp_user = User.objects.create(username='Teacher')
        temp_user.set_password('tea')
        temp_user.save()
        SchoolUser.objects.create(site_user=temp_user, type_user='T')

        temp_user = User.objects.create(username='Student')
        temp_user.set_password('stu')
        temp_user.save()
        SchoolUser.objects.create(site_user=temp_user, type_user='S')

        temp_user = User.objects.create(username='Undetermined')
        temp_user.set_password('und')
        temp_user.save()
        SchoolUser.objects.create(site_user=temp_user, type_user='U')

    def test_school_announcement_general_status_check(self):
        temp_client = Client()
        temp_resp = temp_client.get("/school/anno")
        self.assertEqual(temp_resp.status_code, 200)

    def test_school_announcement_general_status_check_reverse(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('school:anno_general'))
        self.assertEqual(temp_resp.status_code, 200)

    def test_school_announcement_general_create_anno_button_show(self):
        temp_client = Client()
        temp_client.login(username='Teacher', password='tea')
        temp_resp = temp_client.get("/school/anno")
        self.assertContains(temp_resp, 'Create new announcement')

        temp_client.logout()
        temp_client.login(username='Admin', password='adm')
        temp_resp = temp_client.get("/school/anno")
        self.assertContains(temp_resp, 'Create new announcement')

    def test_school_announcement_general_create_anno_button_not_show(self):
        temp_client = Client()
        temp_resp = temp_client.get("/school/anno")
        self.assertNotContains(temp_resp, 'Create new announcement')

        temp_client.login(username='Student', password='stu')
        temp_resp = temp_client.get("/school/anno")
        self.assertNotContains(temp_resp, 'Create new announcement')

        temp_client.logout()
        temp_client.login(username='Undetermined', password='und')
        temp_resp = temp_client.get("/school/anno")
        self.assertNotContains(temp_resp, 'Create new announcement')

    def test_school_announcement_general_show_created_announcement(self):
        temp_client = Client()
        temp_resp = temp_client.get("/school/anno")
        self.assertContains(temp_resp, 'title')
        self.assertContains(temp_resp, 'content')


class CheckSchoolViewAnnoDetail(TestCase):
    @classmethod
    def setUp(self):
        temp_user = User.objects.create(username='Admin')
        temp_user.set_password('adm')
        temp_user.save()
        SchoolUser.objects.create(site_user=temp_user, type_user='A')

        temp_user = User.objects.create(username='Teacher')
        temp_user.set_password('tea')
        temp_user.save()
        temp_schooluser = SchoolUser.objects.create(site_user=temp_user, type_user='T')

        Announcement.objects.create(anno_title='title', anno_content='content', anno_date=datetime.now(), auther_name=temp_schooluser)

        temp_user = User.objects.create(username='OtherTeacher')
        temp_user.set_password('tea')
        temp_user.save()
        SchoolUser.objects.create(site_user=temp_user, type_user='T')

        temp_user = User.objects.create(username='Student')
        temp_user.set_password('stu')
        temp_user.save()
        SchoolUser.objects.create(site_user=temp_user, type_user='S')

        temp_user = User.objects.create(username='Undetermined')
        temp_user.set_password('und')
        temp_user.save()
        SchoolUser.objects.create(site_user=temp_user, type_user='U')

    def test_school_announcement_detail_status_check_created(self):
        temp_client = Client()
        temp_resp = temp_client.get("/school/anno/1")
        self.assertEqual(temp_resp.status_code, 200)

    def test_school_announcement_detail_status_check_not_created(self):
        temp_client = Client()
        temp_resp = temp_client.get("/school/anno/2")
        self.assertEqual(temp_resp.status_code, 404)

    def test_school_announcement_detail_status_check_reverse(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('school:anno_detail', kwargs={'pk':1}))
        self.assertEqual(temp_resp.status_code, 200)

    def test_school_announcement_detail_update_button_show(self):
        temp_client = Client()
        temp_client.login(username='Admin', password='adm')
        temp_resp = temp_client.get("/school/anno/1")
        self.assertContains(temp_resp, 'Update')
        self.assertContains(temp_resp, 'Delete')

        temp_client.logout()
        temp_client.login(username='Teacher', password='tea')
        temp_resp = temp_client.get("/school/anno/1")
        self.assertContains(temp_resp, 'Update')
        self.assertContains(temp_resp, 'Delete')

    def test_school_announcement_detail_update_button_not_show(self):
        temp_client = Client()
        temp_resp = temp_client.get("/school/anno/1")
        self.assertNotContains(temp_resp, 'Update')
        self.assertNotContains(temp_resp, 'Delete')
        
        temp_client.login(username='OtherTeacher', password='tea')
        temp_resp = temp_client.get("/school/anno/1")
        self.assertNotContains(temp_resp, 'Update')
        self.assertNotContains(temp_resp, 'Delete')

        temp_client.logout()
        temp_client.login(username='Student', password='stu')
        temp_resp = temp_client.get("/school/anno/1")
        self.assertNotContains(temp_resp, 'Update')
        self.assertNotContains(temp_resp, 'Delete')

        temp_client.logout()
        temp_client.login(username='Undetermined', password='und')
        temp_resp = temp_client.get("/school/anno/1")
        self.assertNotContains(temp_resp, 'Update')
        self.assertNotContains(temp_resp, 'Delete')


class CheckSchoolViewAnnoCreate(TestCase):
    def setUp(self):
        temp_user = User.objects.create(username='Admin')
        temp_user.set_password('adm')
        temp_user.save()
        SchoolUser.objects.create(site_user=temp_user, type_user='A')

        temp_user = User.objects.create(username='Teacher')
        temp_user.set_password('tea')
        temp_user.save()
        SchoolUser.objects.create(site_user=temp_user, type_user='T')

        temp_user = User.objects.create(username='Student')
        temp_user.set_password('stu')
        temp_user.save()
        SchoolUser.objects.create(site_user=temp_user, type_user='S')

        temp_user = User.objects.create(username='Undetermined')
        temp_user.set_password('und')
        temp_user.save()
        SchoolUser.objects.create(site_user=temp_user, type_user='U')

    def test_school_announcement_create_status_check_allowed(self):
        temp_client = Client()
        temp_client.login(username='Admin', password='adm')
        temp_resp = temp_client.get("/school/anno/create")
        self.assertEqual(temp_resp.status_code, 200)
        
        temp_client.logout()
        temp_client.login(username='Teacher', password='tea')
        temp_resp = temp_client.get("/school/anno/create")
        self.assertEqual(temp_resp.status_code, 200)

        temp_client.logout()
        temp_client.login(username='Student', password='stu')
        temp_resp = temp_client.get("/school/anno/create")
        self.assertEqual(temp_resp.status_code, 200)

        temp_client.logout()
        temp_client.login(username='Undetermined', password='und')
        temp_resp = temp_client.get("/school/anno/create")
        self.assertEqual(temp_resp.status_code, 200)

        temp_client.logout()
        temp_client = Client()
        temp_resp = temp_client.get("/school/anno/create")
        self.assertEqual(temp_resp.status_code, 302)

    def test_school_announcement_create_status_check_reverse(self):
        temp_client = Client()
        temp_resp = temp_client.get(reverse('school:anno_create'))
        self.assertEqual(temp_resp.status_code, 302)

