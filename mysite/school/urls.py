from django.urls import path
from . import views


app_name = "school"


urlpatterns = [
    path('', views.SchoolMainView.as_view(), name='school_main'),

    path('teacher', views.TeacherGeneralView.as_view(), name='teacher_general'),
    path('teacher/<int:pk>', views.TeacherDetailView.as_view(), name='teacher_detail'),

    path('student', views.StudentGeneralView.as_view(), name='student_general'),
    path('student/<int:pk>', views.StudentDetailView.as_view(), name='student_detail'),

    path('anno', views.AnnoGeneralView.as_view(), name='anno_general'),
    path('anno/<int:pk>', views.AnnoDetailView.as_view(), name='anno_detail'),
    path('anno/create', views.AnnoCreateView.as_view(), name='anno_create'),
    path('anno/<int:pk>/update', views.AnnoUpdateView.as_view(), name='anno_update'),
    path('anno/<int:pk>/delete', views.AnnoDeleteView.as_view(), name='anno_delete'),

    path('admin/register', views.AdminRegisterListView.as_view(), name='register_general'),
    path('admin/register/<int:pk>', views.AdminRegisterUpdateView.as_view(), name='register_update'),

    path('test/<int:pk>', views.TestClassView.as_view(), name='test_detail'),
]
