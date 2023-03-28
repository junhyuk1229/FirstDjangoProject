from django.contrib import admin
from . import models

admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.Announcement)
admin.site.register(models.SchoolUser)
admin.site.register(models.Subject)
admin.site.register(models.SchoolClass)
admin.site.register(models.ClassStudentRelation)

