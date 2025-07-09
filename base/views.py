from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm,CourseForm, LessonForm, LiveClassForm
from .models import Course, Lesson, LiveClass, Progress, Enrollment, LessonProgress
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request,'home.html')

def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')
        
            # messages.error(request, "Please correct the errors below.")
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if request.user.role == 'student':
                return redirect('student_dashboard')
            elif request.user.role == 'teacher':
                return redirect('dashboard')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.role == 'student':
        return render(request, 'student_dashboard.html')
    elif request.user.role == 'teacher':
        return render(request, 'teacher_dashboard.html')
    else:
        return render(request, 'home.html')



# Only for teachers
def is_teacher(user):
    return user.role == 'teacher'

@login_required
@user_passes_test(is_teacher)
def create_course(request):
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect('dashboard')
    return render(request, 'create_course.html', {'form': form})

@login_required
@user_passes_test(is_teacher)
def upload_lesson(request):
    form = LessonForm()
    form.fields['course'].queryset = Course.objects.filter(teacher=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    return render(request, 'upload_lesson.html', {'form': form})

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

@login_required
@user_passes_test(is_teacher)
def course_detail(request, slug):
    course = Course.objects.get(slug=slug)
    lessons = course.lessons.all()
    return render(request, 'course_detail.html', {'course': course, 'lessons': lessons})




@login_required
@user_passes_test(is_teacher)
def schedule_live_class(request):
    form = LiveClassForm(user=request.user)
    if request.method == 'POST':
        form = LiveClassForm(request.POST, user=request.user)
        if form.is_valid():
            live_class = form.save(commit=False)
            live_class.created_by = request.user
            live_class.save()
            return redirect('dashboard')
    return render(request, 'schedule_live_class.html', {'form': form})

@login_required
@user_passes_test(is_teacher)
def upcoming_classes(request):
    now = timezone.now()
    classes = LiveClass.objects.filter(scheduled_datetime__gte=now).order_by('scheduled_datetime')
    return render(request, 'upcoming_classes.html', {'classes': classes})

@login_required
def update_progress(request, course_id, lesson_id):
    course = Course.objects.get(id=course_id)
    lesson = Lesson.objects.get(id=lesson_id)
    progress, created = Progress.objects.get_or_create(student=request.user, course=course)
    progress.completed_lessons.add(lesson)
    return redirect('course_detail', slug=course.slug)



#student
def is_student(user):
    return user.role == 'student'
@login_required
@user_passes_test(is_student)
def student_course_list(request):
    courses = Course.objects.all()
    return render(request, 'student_course_list.html', {'courses': courses})
@login_required
@user_passes_test(is_student)
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('student_dashboard')

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'student_dashboard.html', {'enrollments': enrollments})

@login_required
@user_passes_test(is_student)
def student_course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    progress = LessonProgress.objects.filter(student=request.user, lesson__in=lessons)
    completed_lessons = progress.filter(completed=True).values_list('lesson_id', flat=True)
    return render(request, 'student_course_detail.html', {
        'course': course,
        'lessons': lessons,
        'completed_lessons': completed_lessons
    })

@login_required
@user_passes_test(is_student)
def mark_lesson_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, created = LessonProgress.objects.get_or_create(student=request.user, lesson=lesson)
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()
    return redirect('student_course_detail', course_id=lesson.course.id)

@login_required
@user_passes_test(is_student)
def student_upcoming_classes(request):
    enrollments = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
    classes = LiveClass.objects.filter(course__id__in=enrollments, scheduled_datetime__gte=timezone.now()).order_by('scheduled_datetime')
    return render(request, 'student_upcoming_classes.html', {'classes': classes})
