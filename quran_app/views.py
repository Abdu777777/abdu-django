import os
from django.http import HttpResponse, Http404

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Teacher, Halaqa, Student, Progress, Attendance
from .forms import UserRegisterForm, TeacherForm, HalaqaForm, StudentForm, ProgressForm, AttendanceForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        if form.is_valid() and teacher_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()
            messages.success(request, f'تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.')
            return redirect('login')
    else:
        form = UserRegisterForm()
        teacher_form = TeacherForm()
    return render(request, 'quran_app/register.html', {'form': form, 'teacher_form': teacher_form})

@login_required
def home(request):
    try:
        teacher = request.user.teacher
        halaqat_count = Halaqa.objects.filter(teacher=teacher).count()
        students_count = Student.objects.filter(halaqa__teacher=teacher).count()
        recent_progress = Progress.objects.filter(student__halaqa__teacher=teacher).order_by('-date')[:5]
        
        context = {
            'halaqat_count': halaqat_count,
            'students_count': students_count,
            'recent_progress': recent_progress,
            'teacher': teacher
        }
    except Teacher.DoesNotExist:
        context = {'is_admin': request.user.is_superuser}
        
    return render(request, 'quran_app/home.html', context)

# CRUD for Halaqa
@login_required
def halaqa_list(request):
    halaqat = Halaqa.objects.filter(teacher=request.user.teacher)
    return render(request, 'quran_app/halaqa_list.html', {'halaqat': halaqat})

@login_required
def halaqa_create(request):
    if request.method == 'POST':
        form = HalaqaForm(request.POST)
        if form.is_valid():
            halaqa = form.save(commit=False)
            halaqa.teacher = request.user.teacher
            halaqa.save()
            messages.success(request, "تمت إضافة الحلقة بنجاح")
            return redirect('halaqa_list')
    else:
        form = HalaqaForm()
    return render(request, 'quran_app/halaqa_form.html', {'form': form, 'title': 'إضافة حلقة جديدة'})

@login_required
def halaqa_update(request, pk):
    halaqa = get_object_or_404(Halaqa, pk=pk)
    if request.method == 'POST':
        form = HalaqaForm(request.POST, instance=halaqa)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث بيانات الحلقة")
            return redirect('halaqa_list')
    else:
        form = HalaqaForm(instance=halaqa)
    return render(request, 'quran_app/halaqa_form.html', {'form': form, 'title': 'تعديل حلقة'})

@login_required
def halaqa_delete(request, pk):
    halaqa = get_object_or_404(Halaqa, pk=pk, teacher=request.user.teacher)
    if request.method == 'POST':
        halaqa.delete()
        messages.success(request, "تم حذف الحلقة")
        return redirect('halaqa_list')
    return render(request, 'quran_app/confirm_delete.html', {'object': halaqa})

# CRUD for Student
@login_required
def student_list(request):
    students = Student.objects.filter(halaqa__teacher=request.user.teacher)
    return render(request, 'quran_app/student_list.html', {'students': students})

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, "تم تسجيل الطالب بنجاح")
            return redirect('student_list')
    else:
        form = StudentForm()
        # تقييد الخيارات للحلقات التابعة للمعلم الحالي فقط
        form.fields['halaqa'].queryset = Halaqa.objects.filter(teacher=request.user.teacher)
    return render(request, 'quran_app/student_form.html', {'form': form, 'title': 'إضافة طالب جديد'})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث بيانات الطالب")
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
        form.fields['halaqa'].queryset = Halaqa.objects.filter(teacher=request.user.teacher)
    return render(request, 'quran_app/student_form.html', {'form': form, 'title': 'تعديل بيانات طالب'})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk, halaqa__teacher=request.user.teacher)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "تم حذف الطالب")
        return redirect('student_list')
    return render(request, 'quran_app/confirm_delete.html', {'object': student})

# CRUD for Progress
@login_required
def progress_list(request):
    records = Progress.objects.filter(student__halaqa__teacher=request.user.teacher).order_by('-date')
    return render(request, 'quran_app/progress_list.html', {'records': records})

@login_required
def progress_create(request):
    if request.method == 'POST':
        form = ProgressForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تسجيل التسميع بنجاح")
            return redirect('progress_list')
    else:
        form = ProgressForm()
        form.fields['student'].queryset = Student.objects.filter(halaqa__teacher=request.user.teacher)
    return render(request, 'quran_app/progress_form.html', {'form': form, 'title': 'تسجيل تسميع جديد'})

@login_required
def progress_update(request, pk):
    record = get_object_or_404(Progress, pk=pk, student__halaqa__teacher=request.user.teacher)
    if request.method == 'POST':
        form = ProgressForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث سجل التسميع")
            return redirect('progress_list')
    else:
        form = ProgressForm(instance=record)
        form.fields['student'].queryset = Student.objects.filter(halaqa__teacher=request.user.teacher)
    return render(request, 'quran_app/progress_form.html', {'form': form, 'title': 'تعديل سجل تسميع'})

@login_required
def progress_delete(request, pk):
    record = get_object_or_404(Progress, pk=pk, student__halaqa__teacher=request.user.teacher)
    if request.method == 'POST':
        record.delete()
        messages.success(request, "تم حذف السجل")
        return redirect('progress_list')
    return render(request, 'quran_app/confirm_delete.html', {'object': record})

# CRUD for Attendance
@login_required
def attendance_list(request):
    records = Attendance.objects.filter(student__halaqa__teacher=request.user.teacher).order_by('-date')
    return render(request, 'quran_app/attendance_list.html', {'records': records})

@login_required
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تسجيل الحضور بنجاح")
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
        form.fields['student'].queryset = Student.objects.filter(halaqa__teacher=request.user.teacher)
    return render(request, 'quran_app/attendance_form.html', {'form': form, 'title': 'تسجيل حضور جديد'})

@login_required
def attendance_update(request, pk):
    record = get_object_or_404(Attendance, pk=pk, student__halaqa__teacher=request.user.teacher)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث سجل الحضور")
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=record)
        form.fields['student'].queryset = Student.objects.filter(halaqa__teacher=request.user.teacher)
    return render(request, 'quran_app/attendance_form.html', {'form': form, 'title': 'تعديل سجل حضور'})

@login_required
def attendance_delete(request, pk):
    record = get_object_or_404(Attendance, pk=pk, student__halaqa__teacher=request.user.teacher)
    if request.method == 'POST':
        record.delete()
        messages.success(request, "تم حذف سجل الحضور")
        return redirect('attendance_list')
    return render(request, 'quran_app/confirm_delete.html', {'object': record})
@login_required
def download_file(request):
    # Vulnerability: Path Traversal
    file_path = request.GET.get('path', '')
    if not file_path:
        return HttpResponse("Please provide a path parameter", status=400)

    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=404)
