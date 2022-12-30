from django.shortcuts import render, HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Teacher, Student, Announcement


def main_page(request):
    context = {
        'announcements': Announcement.objects.all()
    }

    return render(request, "school/main_page.html", context)


class AnnoListView(generic.ListView):
    template_name = 'school/main_page.html'
    model = Announcement
    context_object_name = 'announcements'
    ordering = ['-date_posted']

    def get_queryset(self):
        return Announcement.objects.all()


class AnnoDetailView(generic.DetailView):
    template_name = 'school/anno_detail.html'
    model = Announcement


class AnnoCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'school/anno_create.html'
    model = Announcement
    fields = ['anno_title', 'anno_content']

    def form_valid(self, form):
        form.instance.auther_name = self.request.user
        return super().form_valid(form)


class AnnoUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    template_name = 'school/anno_update.html'
    model = Announcement
    fields = ['anno_title', 'anno_content']

    def form_valid(self, form):
        form.instance.auther_name = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        anno = self.get_object()
        if self.request.user == anno.auther_name:
            return True
        return False


class AnnoDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    template_name = 'school/anno_delete.html'
    model = Announcement
    success_url = '/'

    def test_func(self):
        anno = self.get_object()
        if self.request.user == anno.auther_name:
            return True
        return False


class TeacherGeneralView(generic.ListView):
    template_name = 'school/teacher_generic.html'
    context_object_name = 'teacher_list'

    def get_queryset(self):
        return Teacher.objects.all()


class StudentGeneralView(generic.ListView):
    template_name = 'school/student_generic.html'
    context_object_name = 'student_list'

    def get_queryset(self):
        return Student.objects.all()


class TeacherDetailView(generic.DetailView):
    model = Teacher
    template_name = 'school/teacher_detail.html'


class StudentDetailView(generic.DetailView):
    model = Student
    template_name = 'school/student_detail.html'
