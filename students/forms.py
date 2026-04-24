from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import ExamSchedule, Schedule, Score, Student, Subject


class DateInput(forms.DateInput):
    input_type = "date"


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {css_class}".strip()


class StudentAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    username = forms.CharField(label="Tên đăng nhập")
    password = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput)


class StudentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "user",
            "student_code",
            "full_name",
            "date_of_birth",
            "gender",
            "class_name",
            "email",
            "phone_number",
            "address",
            "bio",
            "avatar",
        ]
        widgets = {
            "date_of_birth": DateInput(),
        }


class SubjectForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["subject_code", "name", "credits"]


class ScoreForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Score
        fields = [
            "student",
            "subject",
            "attendance_score",
            "midterm_score",
            "final_exam_score",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = Student.objects.order_by("student_code")
        self.fields["subject"].queryset = Subject.objects.order_by("subject_code")


class ScheduleForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Schedule
        fields = [
            "student",
            "subject",
            "weekday",
            "effective_from",
            "effective_to",
            "room",
            "start_time",
            "end_time",
            "note",
        ]
        widgets = {
            "effective_from": DateInput(),
            "effective_to": DateInput(),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = Student.objects.order_by("student_code")
        self.fields["subject"].queryset = Subject.objects.order_by("subject_code")


class ExamScheduleForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ExamSchedule
        fields = [
            "student",
            "subject",
            "exam_date",
            "start_time",
            "room",
            "seat_number",
            "note",
        ]
        widgets = {
            "exam_date": DateInput(),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = Student.objects.order_by("student_code")
        self.fields["subject"].queryset = Subject.objects.order_by("subject_code")


class StudentProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "full_name",
            "date_of_birth",
            "gender",
            "email",
            "phone_number",
            "address",
            "bio",
            "avatar",
        ]
        widgets = {
            "date_of_birth": DateInput(),
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
