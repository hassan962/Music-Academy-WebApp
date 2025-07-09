from django.contrib import admin
from .models import User, Course, Lesson, LiveClass, Progress, Enrollment, LessonProgress
# Register your models here.


admin.site.register(User)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(LiveClass)
admin.site.register(Progress)
admin.site.register(Enrollment)
admin.site.register(LessonProgress)
