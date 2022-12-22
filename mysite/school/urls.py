from django.urls import path
from . import views


app_name = "school"


urlpatterns = [
    path('', views.main_page, name='school_main'),
    path('teacher', views.TeacherGeneralView.as_view(), name='teacher_general'),
    path('student', views.StudentGeneralView.as_view(), name='student_general'),
    path('teacher/<int:pk>', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('student/<int:pk>', views.StudentDetailView.as_view(), name='student_detail'),
]