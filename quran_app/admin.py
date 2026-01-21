from django.contrib import admin
from .models import Teacher, Halaqa, Student, Progress, Attendance

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'specialization', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')

@admin.register(Halaqa)
class HalaqaAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'days', 'time', 'location')
    list_filter = ('days', 'teacher')
    search_fields = ('name', 'location')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'halaqa', 'phone', 'join_date')
    list_filter = ('halaqa',)
    search_fields = ('name', 'phone')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'surah', 'grade', 'date')
    list_filter = ('grade', 'date')
    search_fields = ('student__name', 'surah')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('student__name',)
