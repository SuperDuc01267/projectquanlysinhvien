from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from .models import ExamSchedule, Schedule, Score, Student, Subject


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    change_list_template = "admin/students/student/change_list.html"
    change_form_template = "admin/students/student/change_form.html"
    list_display = (
        "account_badge",
        "student_code",
        "full_name",
        "class_name_badge",
        "gender_badge",
        "email",
        "average_score_badge",
        "academic_classification_badge",
    )
    search_fields = ("student_code", "full_name", "class_name", "email", "user__username")
    list_filter = ("gender", "class_name")
    ordering = ("student_code",)
    list_per_page = 12
    fieldsets = (
        ("Thong tin tai khoan", {"fields": ("user",)}),
        (
            "Thong tin sinh vien",
            {
                "fields": (
                    "student_code",
                    "full_name",
                    "date_of_birth",
                    "gender",
                    "class_name",
                    "email",
                )
            },
        ),
    )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        total_students = Student.objects.count()
        linked_accounts = Student.objects.exclude(user__isnull=True).count()
        by_class = (
            Student.objects.values("class_name")
            .annotate(total=Count("id"))
            .order_by("-total", "class_name")[:5]
        )
        extra_context["student_summary"] = {
            "total_students": total_students,
            "linked_accounts": linked_accounts,
            "unlinked_accounts": total_students - linked_accounts,
            "top_classes": by_class,
        }
        return super().changelist_view(request, extra_context=extra_context)

    def account_badge(self, obj):
        if obj.user:
            return format_html(
                '<span class="admin-badge admin-badge-success">@{}</span>',
                obj.user.username,
            )
        return format_html(
            '<span class="admin-badge admin-badge-muted">{}</span>',
            "Chua lien ket",
        )

    account_badge.short_description = "Tai khoan"
    account_badge.admin_order_field = "user__username"

    def class_name_badge(self, obj):
        return format_html('<span class="admin-badge admin-badge-info">{}</span>', obj.class_name)

    class_name_badge.short_description = "Lop"
    class_name_badge.admin_order_field = "class_name"

    def gender_badge(self, obj):
        return format_html(
            '<span class="admin-badge admin-badge-muted">{}</span>',
            obj.get_gender_display(),
        )

    gender_badge.short_description = "Gioi tinh"
    gender_badge.admin_order_field = "gender"

    def average_score_badge(self, obj):
        score_text = f"{obj.average_score():.2f}"
        return format_html(
            '<span class="admin-badge admin-badge-score">{}</span>',
            score_text,
        )

    average_score_badge.short_description = "Diem TB"

    def academic_classification_badge(self, obj):
        classification = obj.academic_classification()
        css_class = {
            "Gioi": "admin-badge-success",
            "Kha": "admin-badge-info",
            "Trung binh": "admin-badge-warning",
            "Yeu": "admin-badge-danger",
        }.get(classification, "admin-badge-muted")
        return format_html('<span class="admin-badge {}">{}</span>', css_class, classification)

    academic_classification_badge.short_description = "Hoc luc"

    class Media:
        css = {"all": ("admin/students-admin.css",)}


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("subject_code", "name", "credits")
    search_fields = ("subject_code", "name")
    list_filter = ("credits",)
    ordering = ("subject_code",)


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "subject",
        "attendance_score",
        "midterm_score",
        "final_exam_score",
        "final_score",
        "updated_at",
    )
    search_fields = (
        "student__student_code",
        "student__full_name",
        "subject__subject_code",
        "subject__name",
    )
    list_filter = ("subject", "student__class_name")
    autocomplete_fields = ("student", "subject")
    readonly_fields = ("final_score", "created_at", "updated_at")
    ordering = ("student__student_code", "subject__subject_code")


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "weekday", "room", "start_time", "end_time")
    search_fields = (
        "student__student_code",
        "student__full_name",
        "subject__subject_code",
        "subject__name",
        "room",
    )
    list_filter = ("weekday", "room")
    autocomplete_fields = ("student", "subject")
    ordering = ("student__student_code", "weekday", "start_time")


@admin.register(ExamSchedule)
class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "exam_date", "start_time", "room", "seat_number")
    search_fields = (
        "student__student_code",
        "student__full_name",
        "subject__subject_code",
        "subject__name",
        "room",
        "seat_number",
    )
    list_filter = ("exam_date", "room")
    autocomplete_fields = ("student", "subject")
    ordering = ("student__student_code", "exam_date", "start_time")
