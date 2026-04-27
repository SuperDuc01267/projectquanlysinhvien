from decimal import Decimal, ROUND_HALF_UP
from datetime import timedelta

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone


def default_schedule_end_date():
    return timezone.localdate() + timedelta(days=120)


class Student(models.Model):
    GENDER_CHOICES = (
        ("M", "Nam"),
        ("F", "Nu"),
        ("O", "Khac"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_profile",
        verbose_name="Tài khoản đăng nhập",
    )
    student_code = models.CharField(max_length=20, unique=True, verbose_name="Ma sinh vien")
    full_name = models.CharField(max_length=100, verbose_name="Ho ten")
    date_of_birth = models.DateField(verbose_name="Ngay sinh")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Gioi tinh")
    class_name = models.CharField(max_length=50, verbose_name="Lop")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="So dien thoai")
    address = models.CharField(max_length=255, blank=True, verbose_name="Dia chi")
    bio = models.TextField(blank=True, verbose_name="Gioi thieu ban than")
    avatar = models.FileField(upload_to="avatars/", blank=True, null=True, verbose_name="Anh dai dien")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["student_code"]
        verbose_name = "Sinh vien"
        verbose_name_plural = "Sinh vien"

    def __str__(self):
        return f"{self.student_code} - {self.full_name}"

    def average_score(self):
        average = self.scores.aggregate(avg=Avg("final_score"))["avg"]
        return round(average or 0, 2)

    def academic_classification(self):
        average = self.average_score()
        if average >= 8.5:
            return "Gioi"
        if average >= 7.0:
            return "Kha"
        if average >= 5.0:
            return "Trung binh"
        return "Yeu"


class Subject(models.Model):
    subject_code = models.CharField(max_length=20, unique=True, verbose_name="Ma mon hoc")
    name = models.CharField(max_length=100, verbose_name="Ten mon hoc")
    credits = models.PositiveSmallIntegerField(verbose_name="So tin chi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["subject_code"]
        verbose_name = "Mon hoc"
        verbose_name_plural = "Mon hoc"

    def __str__(self):
        return f"{self.subject_code} - {self.name}"


class Score(models.Model):
    score_validators = [MinValueValidator(0), MaxValueValidator(10)]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="scores",
        verbose_name="Sinh vien",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="scores",
        verbose_name="Mon hoc",
    )
    attendance_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=score_validators,
        verbose_name="Diem qua trinh",
    )
    midterm_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=score_validators,
        verbose_name="Diem giua ky",
    )
    final_exam_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=score_validators,
        verbose_name="Diem cuoi ky",
    )
    final_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        editable=False,
        verbose_name="Diem tong ket",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["student__student_code", "subject__subject_code"]
        verbose_name = "Bang diem"
        verbose_name_plural = "Bang diem"
        constraints = [
            models.UniqueConstraint(
                fields=["student", "subject"],
                name="unique_student_subject_score",
            )
        ]

    def __str__(self):
        return f"{self.student.student_code} - {self.subject.subject_code}"

    def calculate_final_score(self):
        total = (
            Decimal(self.attendance_score) * Decimal("0.2")
            + Decimal(self.midterm_score) * Decimal("0.2")
            + Decimal(self.final_exam_score) * Decimal("0.6")
        )
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def save(self, *args, **kwargs):
        self.final_score = self.calculate_final_score()
        super().save(*args, **kwargs)


class Schedule(models.Model):
    WEEKDAY_CHOICES = (
        ("2", "Thứ 2"),
        ("3", "Thứ 3"),
        ("4", "Thứ 4"),
        ("5", "Thứ 5"),
        ("6", "Thứ 6"),
        ("7", "Thứ 7"),
        ("CN", "Chủ nhật"),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name="Sinh viên",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name="Môn học",
    )
    weekday = models.CharField(max_length=2, choices=WEEKDAY_CHOICES, verbose_name="Thứ")
    effective_from = models.DateField(verbose_name="Hiệu lực từ", default=timezone.localdate)
    effective_to = models.DateField(
        verbose_name="Hiệu lực đến",
        blank=True,
        default=default_schedule_end_date,
    )
    room = models.CharField(max_length=50, verbose_name="Phòng học")
    start_time = models.TimeField(verbose_name="Giờ bắt đầu")
    end_time = models.TimeField(verbose_name="Giờ kết thúc")
    note = models.CharField(max_length=255, blank=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["student__student_code", "weekday", "start_time"]
        verbose_name = "Thời khóa biểu"
        verbose_name_plural = "Thời khóa biểu"
        constraints = [
            models.UniqueConstraint(
                fields=["student", "subject", "weekday", "start_time"],
                name="unique_student_schedule_slot",
            )
        ]

    def __str__(self):
        return f"{self.student.student_code} - {self.subject.name} - {self.get_weekday_display()}"

    def save(self, *args, **kwargs):
        if not self.effective_to:
            self.effective_to = self.effective_from + timedelta(days=120)
        super().save(*args, **kwargs)


class ExamSchedule(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="exam_schedules",
        verbose_name="Sinh viên",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="exam_schedules",
        verbose_name="Môn học",
    )
    exam_date = models.DateField(verbose_name="Ngày thi")
    start_time = models.TimeField(verbose_name="Giờ bắt đầu")
    room = models.CharField(max_length=50, verbose_name="Phòng thi")
    seat_number = models.CharField(max_length=20, blank=True, verbose_name="Số báo danh")
    note = models.CharField(max_length=255, blank=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["student__student_code", "exam_date", "start_time"]
        verbose_name = "Lịch thi"
        verbose_name_plural = "Lịch thi"
        constraints = [
            models.UniqueConstraint(
                fields=["student", "subject", "exam_date", "start_time"],
                name="unique_student_exam_slot",
            )
        ]

    def __str__(self):
        return f"{self.student.student_code} - {self.subject.name} - {self.exam_date}"
