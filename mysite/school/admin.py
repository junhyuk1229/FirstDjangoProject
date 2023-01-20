from django.contrib import admin
from .models import Student, Teacher, Announcement, SchoolUser

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Announcement)
admin.site.register(SchoolUser)