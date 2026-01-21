from django import forms
from django.contrib.auth.models import User
from .models import Teacher, Halaqa, Student, Progress, Attendance

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'كلمة المرور'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تأكيد كلمة المرور'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المستخدم'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم الأول'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم الأخير'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("كلمات المرور غير متطابقة")
        return confirm_password

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['phone', 'specialization']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'التخصص أو الإجازة'}),
        }

class HalaqaForm(forms.ModelForm):
    class Meta:
        model = Halaqa
        fields = ['name', 'days', 'time', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'days': forms.Select(attrs={'class': 'form-select'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'halaqa', 'phone', 'birth_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'halaqa': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['student', 'surah', 'from_ayah', 'to_ayah', 'grade', 'notes']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'surah': forms.TextInput(attrs={'class': 'form-control'}),
            'from_ayah': forms.NumberInput(attrs={'class': 'form-control'}),
            'to_ayah': forms.NumberInput(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
