from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    phone = models.CharField(max_length=15, verbose_name="رقم الهاتف")
    specialization = models.CharField(max_length=100, verbose_name="التخصص/الإجازة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الانضمام")

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = "معلم"
        verbose_name_plural = "المعلمون"

class Halaqa(models.Model):
    DAYS_CHOICES = [
        ('يومي', 'يومي'),
        ('سبت-اثنين-أربعاء', 'سبت-اثنين-أربعاء'),
        ('أحد-ثلاثاء-خميس', 'أحد-ثلاثاء-خميس'),
    ]
    name = models.CharField(max_length=100, verbose_name="اسم الحلقة")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='halaqat', verbose_name="المعلم")
    days = models.CharField(max_length=50, choices=DAYS_CHOICES, default='يومي', verbose_name="أيام الحلقة")
    time = models.TimeField(verbose_name="وقت الحلقة")
    location = models.CharField(max_length=100, verbose_name="المكان")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "حلقة"
        verbose_name_plural = "الحلقات"

class Student(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم الطالب")
    halaqa = models.ForeignKey(Halaqa, on_delete=models.CASCADE, related_name='students', verbose_name="الحلقة")
    phone = models.CharField(max_length=15, verbose_name="رقم هاتف ولي الأمر")
    birth_date = models.DateField(verbose_name="تاريخ الميلاد")
    join_date = models.DateField(auto_now_add=True, verbose_name="تاريخ التسجيل")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "طالب"
        verbose_name_plural = "الطلاب"

class Progress(models.Model):
    GRADE_CHOICES = [
        ('ممتاز', 'ممتاز'),
        ('جيد جداً', 'جيد جداً'),
        ('جيد', 'جيد'),
        ('مقبول', 'مقبول'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='progress_records', verbose_name="الطالب")
    date = models.DateField(auto_now_add=True, verbose_name="التاريخ")
    surah = models.CharField(max_length=100, verbose_name="السورة")
    from_ayah = models.PositiveIntegerField(verbose_name="من آية")
    to_ayah = models.PositiveIntegerField(verbose_name="إلى آية")
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, verbose_name="التقييم")
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات المعلم")

    def __str__(self):
        return f"{self.student.name} - {self.surah}"

    class Meta:
        verbose_name = "سجل تسميع"
        verbose_name_plural = "سجلات التسميع"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('حاضر', 'حاضر'),
        ('غائب', 'غائب'),
        ('مستأذن', 'مستأذن'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records', verbose_name="الطالب")
    date = models.DateField(verbose_name="التاريخ")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="الحالة")
    
    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"

    class Meta:
        verbose_name = "سجل حضور"
        verbose_name_plural = "سجلات الحضور"
        unique_together = ('student', 'date')
