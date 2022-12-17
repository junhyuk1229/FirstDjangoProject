from django.shortcuts import render, HttpResponse
from django.views import generic
from .models import Teacher, Student


def main_page(request):
    return render(request, "school/main_page.html")


class TeacherGeneralView(generic.ListView):
    template_name = 'school/teacher_generic.html'
    context_object_name = 'teacher_list'

    def get_queryset(self):
        return Teacher.objects.order_by('teacher_name')


class StudentGeneralView(generic.ListView):
    template_name = 'school/student_generic.html'
    context_object_name = 'student_list'

    def get_queryset(self):
        return Student.objects.order_by('student_name')


class TeacherDetailView(generic.DetailView):
    model = Teacher
    template_name = 'school/teacher_detail.html'


class StudentDetailView(generic.DetailView):
    model = Student
    template_name = 'school/student_detail.html'
