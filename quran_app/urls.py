from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='quran_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Halaqa URLs
    path('halaqat/', views.halaqa_list, name='halaqa_list'),
    path('halaqa/new/', views.halaqa_create, name='halaqa_create'),
    path('halaqa/<int:pk>/edit/', views.halaqa_update, name='halaqa_update'),
    path('halaqa/<int:pk>/delete/', views.halaqa_delete, name='halaqa_delete'),
    
    # Student URLs
    path('students/', views.student_list, name='student_list'),
    path('student/new/', views.student_create, name='student_create'),
    path('student/<int:pk>/edit/', views.student_update, name='student_update'),
    path('student/<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    # Progress URLs
    path('progress/', views.progress_list, name='progress_list'),
    path('progress/new/', views.progress_create, name='progress_create'),
    path('progress/<int:pk>/edit/', views.progress_update, name='progress_update'),
    path('progress/<int:pk>/delete/', views.progress_delete, name='progress_delete'),

    # Attendance URLs
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/new/', views.attendance_create, name='attendance_create'),
    path('attendance/<int:pk>/edit/', views.attendance_update, name='attendance_update'),
    path('attendance/<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),
    path('download/', views.download_file, name='download_file'),
path('download/', views.download_file, name='download_file'),

]
