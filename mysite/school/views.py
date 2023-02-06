from django.shortcuts import render, HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import SchoolUser, Teacher, Student, Announcement


def main_page(request):
    context = {
        'announcements': Announcement.objects.all()
    }

    return render(request, "school/main_page.html", context)


# region BasicView

class ClassBasicListView(generic.ListView):
    def get_context_data(self, **kwargs):
        context = super(ClassBasicListView, self).get_context_data(**kwargs)
        
        if not self.request.user.is_authenticated:
            context['is_undetermined'] = True
            return context
        
        is_teacher = False
        is_student = False
        is_admin = False
        is_undetermined = False

        try:
            temp_query = SchoolUser.objects.get(site_user=self.request.user)
        except:
            temp_query = SchoolUser.objects.create(
                site_user=self.request.user,
                type_user='U'
            )
        
        if temp_query.type_user == 'A':
            is_admin = True
        elif temp_query.type_user == 'T':
            is_teacher = True
        elif temp_query.type_user == 'S':
            is_student = True
        elif temp_query.type_user == 'U':
            is_undetermined = True
        
        context['is_admin'] = is_admin
        context['is_teacher'] = is_teacher
        context['is_student'] = is_student
        context['is_undetermined'] = is_undetermined
        
        return context

class ClassBasicDetailView(generic.DetailView):
    def get_context_data(self, **kwargs):
        context = super(ClassBasicDetailView, self).get_context_data(**kwargs)

        if not self.request.user.is_authenticated:
            context['is_undetermined'] = True
            return context

        is_teacher = False
        is_student = False
        is_admin = False
        is_undetermined = False

        try:
            temp_query = SchoolUser.objects.get(site_user=self.request.user)
        except:
            temp_query = SchoolUser.objects.create(
                site_user=self.request.user,
                type_user='U'
            )
        
        if temp_query.type_user == 'A':
            is_admin = True
        elif temp_query.type_user == 'T':
            is_teacher = True
        elif temp_query.type_user == 'S':
            is_student = True
        elif temp_query.type_user == 'U':
            is_undetermined = True
        
        context['is_admin'] = is_admin
        context['is_teacher'] = is_teacher
        context['is_student'] = is_student
        context['is_undetermined'] = is_undetermined
        
        return context

class ClassBasicUpdateView(generic.UpdateView):
    def get_context_data(self, **kwargs):
        context = super(ClassBasicUpdateView, self).get_context_data(**kwargs)

        if not self.request.user.is_authenticated:
            context['is_undetermined'] = True
            return context

        is_teacher = False
        is_student = False
        is_admin = False
        is_undetermined = False

        try:
            temp_query = SchoolUser.objects.get(site_user=self.request.user)
        except:
            temp_query = SchoolUser.objects.create(
                site_user=self.request.user,
                type_user='U'
            )
        
        if temp_query.type_user == 'A':
            is_admin = True
        elif temp_query.type_user == 'T':
            is_teacher = True
        elif temp_query.type_user == 'S':
            is_student = True
        elif temp_query.type_user == 'U':
            is_undetermined = True
        
        context['is_admin'] = is_admin
        context['is_teacher'] = is_teacher
        context['is_student'] = is_student
        context['is_undetermined'] = is_undetermined
        
        return context

# endregion


# region Announcement

class AnnoDetailView(ClassBasicDetailView):
    template_name = 'school/anno_detail.html'
    model = Announcement

class AnnoCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'school/anno_create.html'
    model = Announcement
    fields = ['anno_title', 'anno_content']

    def form_valid(self, form):
        form.instance.auther_name = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AnnoCreateView, self).get_context_data(**kwargs)

        is_teacher_admin = False
        temp_query = SchoolUser.objects.get(site_user=self.request.user)
        if temp_query.type_user in ['A', 'T']:
            is_teacher_admin = True
        context['is_teacher'] = is_teacher_admin
        return context

class AnnoUpdateView(LoginRequiredMixin, UserPassesTestMixin, ClassBasicUpdateView):
    model = Announcement
    template_name = 'school/anno_update.html'
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

class AnnoGeneralView(ClassBasicListView):
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

class TeacherGeneralView(ClassBasicListView):
    template_name = 'school/teacher_generic.html'
    context_object_name = 'teacher_list'

    def get_queryset(self):
        return Teacher.objects.all()

class TeacherDetailView(ClassBasicDetailView):
    model = Teacher
    template_name = 'school/teacher_detail.html'

# endregion


# region Student

class StudentGeneralView(ClassBasicListView):
    template_name = 'school/student_generic.html'
    context_object_name = 'student_list'

    def get_queryset(self):
        return Student.objects.all()

class StudentDetailView(ClassBasicDetailView):
    model = Student
    template_name = 'school/student_detail.html'

    

# endregion


# region Admin

class AdminRegisterListView(LoginRequiredMixin, ClassBasicListView):
    model = SchoolUser
    context_object_name = 'register_list'
    template_name = 'school/register_generic.html'

    def get_queryset(self):
        return SchoolUser.objects.filter(type_user='U')

class AdminRegisterUpdateView(LoginRequiredMixin, ClassBasicUpdateView):
    model = SchoolUser
    template_name = 'school/register_update.html'
    fields = ['type_user']

    def form_valid(self, form):
        if form.instance.type_user == 'S':
            if not Student.objects.filter(student_user=form.instance):
                temp = Student(student_user=form.instance)
                temp.save()
        elif form.instance.type_user == 'T':
            if not Teacher.objects.filter(teacher_user=form.instance):
                temp = Teacher(teacher_user=form.instance)
                temp.save()
        return super().form_valid(form)

# endregion


class SchoolMainView(ClassBasicListView):
    template_name = 'school/main_page.html'
    model = Announcement
    context_object_name = 'announcements'
    ordering = ['-date_posted']

    def get_queryset(self):
        return Announcement.objects.all()



class TestClassView(ClassBasicDetailView):
    model = Teacher
    template_name = 'school/test.html'
