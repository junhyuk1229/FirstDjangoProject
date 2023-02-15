from django.shortcuts import render, HttpResponse, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import AnonymousUser
from .models import SchoolUser, Teacher, Student, Announcement
from .forms import AnnoCreateForm


def get_context_schooluser(user, context):
    is_admin = False
    is_teacher = False
    is_student = False
    is_undetermined = False
    if not isinstance(user, AnonymousUser):
        try:
            temp_user = SchoolUser.objects.get(site_user=user)
        except SchoolUser.DoesNotExist:
            auto_create_undetermined_schooluser(user, 'U')
            is_undetermined = True
        else:
            if temp_user.type_user == 'A':
                is_admin = True
            elif temp_user.type_user == 'T':
                is_teacher = True
            elif temp_user.type_user == 'S':
                is_student = True
            else:
                is_undetermined = True
    else:
        is_undetermined = True

    context['is_admin'] = is_admin
    context['is_teacher'] = is_teacher
    context['is_student'] = is_student
    context['is_undetermined'] = is_undetermined

    return


def auto_create_undetermined_schooluser(user, user_type):
    SchoolUser.objects.create(site_user=user, type_user=user_type)


# region Announcement

class AnnoDetailView(generic.DetailView):
    model = Announcement
    template_name = 'school/anno_detail.html'
    context_object_name = 'anno'

    def get_context_data(self, **kwargs):
        context = super(AnnoDetailView, self).get_context_data(**kwargs)
        
        get_context_schooluser(self.request.user, context)
        
        return context

class AnnoCreateView(LoginRequiredMixin, generic.CreateView):
    model = Announcement
    template_name = 'school/anno_create.html'
    fields = ['anno_title', 'anno_content']
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.auther_name = SchoolUser.objects.get(site_user=self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AnnoCreateView, self).get_context_data(**kwargs)
        
        get_context_schooluser(self.request.user, context)
        
        return context

class AnnoUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Announcement
    template_name = 'school/anno_update.html'
    fields = ['anno_title', 'anno_content']
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.auther_name.site_user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        anno = self.get_object()
        if self.request.user == anno.auther_name.site_user or SchoolUser.objects.get(site_user=self.request.user).type_user == 'A':
            return True
        return False
    
    def get_context_data(self, **kwargs):
        context = super(AnnoUpdateView, self).get_context_data(**kwargs)
        
        get_context_schooluser(self.request.user, context)
        
        return context

class AnnoDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Announcement
    template_name = 'school/anno_delete.html'
    context_object_name = 'anno'
    success_url = '/school/anno'
    login_url = '/login/'

    def test_func(self):
        anno = self.get_object()
        if self.request.user == anno.auther_name.site_user or SchoolUser.objects.get(site_user=self.request.user).type_user == 'A':
            return True
        return False
    
    def get_context_data(self, **kwargs):
        context = super(AnnoDeleteView, self).get_context_data(**kwargs)
        
        get_context_schooluser(self.request.user, context)
        
        return context

class AnnoGeneralView(generic.ListView):
    model = Announcement
    template_name = 'school/anno_generic.html'
    context_object_name = 'anno_list'

    def get_queryset(self):
        return Announcement.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AnnoGeneralView, self).get_context_data(**kwargs)

        get_context_schooluser(self.request.user, context)
        
        return context

# endregion


# region Teacher

class TeacherGeneralView(generic.ListView):
    model = Teacher
    template_name = 'school/teacher_generic.html'
    context_object_name = 'teacher_list'

    def get_queryset(self):
        return Teacher.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(TeacherGeneralView, self).get_context_data(**kwargs)
        
        get_context_schooluser(self.request.user, context)
        
        return context

class TeacherDetailView(generic.DetailView):
    model = Teacher
    template_name = 'school/teacher_detail.html'
    context_object_name = 'teacher'

    def get_context_data(self, **kwargs):
        context = super(TeacherDetailView, self).get_context_data(**kwargs)
        
        get_context_schooluser(self.request.user, context)
        
        return context

# endregion


# region Student

class StudentGeneralView(generic.ListView):
    model = Student
    template_name = 'school/student_generic.html'
    context_object_name = 'student_list'

    def get_queryset(self):
        return Student.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(StudentGeneralView, self).get_context_data(**kwargs)
        
        get_context_schooluser(self.request.user, context)
        
        return context

class StudentDetailView(generic.DetailView):
    model = Student
    template_name = 'school/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        
        get_context_schooluser(self.request.user, context)
        
        return context

# endregion


# region Admin

class AdminRegisterListView(LoginRequiredMixin, generic.ListView):
    model = SchoolUser
    template_name = 'school/register_generic.html'
    context_object_name = 'register_list'
    login_url = '/login/'

    def get_queryset(self):
        return SchoolUser.objects.filter(type_user='U')
    
    def get_context_data(self, **kwargs):
        context = super(AdminRegisterListView, self).get_context_data(**kwargs)
        
        get_context_schooluser(self.request.user, context)
        
        return context

class AdminRegisterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = SchoolUser
    template_name = 'school/register_update.html'
    context_object_name = 'schooluser'
    fields = ['type_user']
    login_url = '/login/'

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
    
    def get_context_data(self, **kwargs):
        context = super(AdminRegisterUpdateView, self).get_context_data(**kwargs)
        
        get_context_schooluser(self.request.user, context)
        
        return context

# endregion


class SchoolMainView(generic.ListView):
    template_name = 'school/main_page.html'
    model = Announcement
    context_object_name = 'announcement_list'
    ordering = ['-date_posted']

    def get_queryset(self):
        return Announcement.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(SchoolMainView, self).get_context_data(**kwargs)
        
        get_context_schooluser(self.request.user, context)
        
        return context


class TestClassView(generic.DetailView):
    model = Teacher
    template_name = 'school/test.html'
