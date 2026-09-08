from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db import models
from django.utils import timezone
# Create your models here.

# MediaCloudinaryStorage (Cloudinary's own default) assumes every upload is
# an image and rejects anything else with "Invalid image file" - lesson
# videos and PDFs need the resource-type-specific storage classes instead.
# storage=None (the local-dev/no-Cloudinary case) just means "use the
# project's default storage", identical to omitting the kwarg entirely.
if settings.USE_CLOUDINARY:
    from cloudinary_storage.storage import RawMediaCloudinaryStorage, VideoMediaCloudinaryStorage
    LESSON_VIDEO_STORAGE = VideoMediaCloudinaryStorage()
    LESSON_MATERIAL_STORAGE = RawMediaCloudinaryStorage()
else:
    LESSON_VIDEO_STORAGE = None
    LESSON_MATERIAL_STORAGE = None


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.username



class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='lesson_videos/', null=True, blank=True, storage=LESSON_VIDEO_STORAGE)
    material = models.FileField(upload_to='lesson_materials/', null=True, blank=True, storage=LESSON_MATERIAL_STORAGE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class LiveClass(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='live_classes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    scheduled_datetime = models.DateTimeField(null=True, blank=True, default=timezone.now)
    meeting_link = models.URLField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})

    def __str__(self):
        if self.scheduled_datetime:
            return f"{self.title} on {self.scheduled_datetime.strftime('%Y-%m-%d %H:%M')}"
        return self.title

class Progress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_lessons = models.ManyToManyField(Lesson, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(default=timezone.now)

class LessonProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)