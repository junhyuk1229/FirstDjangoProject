from django.urls import path
from . import views


app_name = "school"


urlpatterns = [
    path('', views.AnnoListView.as_view(), name='school_main'),
    path('teacher', views.TeacherGeneralView.as_view(), name='teacher_general'),
    path('student', views.StudentGeneralView.as_view(), name='student_general'),
    path('teacher/<int:pk>', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('student/<int:pk>', views.StudentDetailView.as_view(), name='student_detail'),
    path('anno/<int:pk>', views.AnnoDetailView.as_view(), name='anno_detail'),
    path('anno/create', views.AnnoCreateView.as_view(), name='anno_create'),
    path('anno/<int:pk>/update', views.AnnoUpdateView.as_view(), name='anno_update'),
    path('anno/<int:pk>/delete', views.AnnoDeleteView.as_view(), name='anno_delete'),
]