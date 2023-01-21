from django.shortcuts import render, HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Teacher, Student, Announcement


def main_page(request):
    context = {
        'announcements': Announcement.objects.all()
    }

    return render(request, "school/main_page.html", context)

# region Announcement

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


class AnnoGeneralView(generic.ListView):
    template_name = 'school/anno_generic.html'
    context_object_name = 'anno_list'

    def get_queryset(self):
        return Announcement.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AnnoGeneralView, self).get_context_data(**kwargs)

        is_teacher_admin = False
        if self.request.user in list(map(lambda x: x.teacher_user.site_user, Teacher.objects.all())):
            is_teacher_admin = True
        context['is_teacher'] = is_teacher_admin
        return context

# endregion

# region Teacher

class TeacherGeneralView(generic.ListView):
    template_name = 'school/teacher_generic.html'
    context_object_name = 'teacher_list'

    def get_queryset(self):
        return Teacher.objects.all()


class TeacherDetailView(generic.DetailView):
    model = Teacher
    template_name = 'school/teacher_detail.html'

# endregion

# region Student

class StudentGeneralView(generic.ListView):
    template_name = 'school/student_generic.html'
    context_object_name = 'student_list'

    def get_queryset(self):
        return Student.objects.all()


class StudentDetailView(generic.DetailView):
    model = Student
    template_name = 'school/student_detail.html'

# endregion

class TestDetailView(generic.DetailView):
    model = Teacher
    template_name = 'school/test.html'