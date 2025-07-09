from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('teacher/create-course/', views.create_course, name='create_course'),
    path('teacher/upload-lesson/', views.upload_lesson, name='upload_lesson'),
     path('teacher/schedule-class/', views.schedule_live_class, name='schedule_class'),
    path('upcoming-classes/', views.upcoming_classes, name='upcoming_classes'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/complete/', views.update_progress, name='update_progress'),

    path('student_course_list/', views.student_course_list, name='student_course_list'),
    path('enroll_in_course/<int:course_id>/enroll/', views.enroll_in_course, name='enroll_course'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student_course_detail/<int:course_id>/', views.student_course_detail, name='student_course_detail'),
    path('lessons/<int:lesson_id>/complete/',views.mark_lesson_complete, name='mark_lesson_complete'),
    path('student_upcoming_classes/',views.student_upcoming_classes, name='student_upcoming_classes'),
]


    
    
    
    

