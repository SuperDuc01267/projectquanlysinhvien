from django.urls import path

from . import views


app_name = "students"

urlpatterns = [
    # Nhóm route cho cổng sinh viên.
    path("", views.HomeView.as_view(), name="home"),
    path("dang-nhap/", views.StudentLoginView.as_view(), name="login"),
    path("dang-xuat/", views.StudentLogoutView.as_view(), name="logout"),
    path("trang-ca-nhan/", views.StudentProfileView.as_view(), name="student_profile"),
    path("ket-qua-hoc-tap/", views.StudentResultView.as_view(), name="student_result"),
    # Route xuất kết quả học tập ra Excel/PDF.
    path("ket-qua-hoc-tap/excel/", views.StudentResultExcelView.as_view(), name="student_result_excel"),
    path("ket-qua-hoc-tap/pdf/", views.StudentResultPdfView.as_view(), name="student_result_pdf"),
    path("thoi-khoa-bieu/", views.StudentScheduleView.as_view(), name="student_schedule"),
    # Route xuất thời khóa biểu ra Excel/PDF.
    path("thoi-khoa-bieu/excel/", views.StudentScheduleExcelView.as_view(), name="student_schedule_excel"),
    path("thoi-khoa-bieu/pdf/", views.StudentSchedulePdfView.as_view(), name="student_schedule_pdf"),
    path("lich-thi/", views.StudentExamScheduleView.as_view(), name="student_exam_schedule"),
    # Route xuất lịch thi ra Excel/PDF.
    path("lich-thi/excel/", views.StudentExamScheduleExcelView.as_view(), name="student_exam_schedule_excel"),
    path("lich-thi/pdf/", views.StudentExamSchedulePdfView.as_view(), name="student_exam_schedule_pdf"),
    # Nhóm route CRUD cho admin/staff.
    path("students/", views.StudentListView.as_view(), name="student_list"),
    path("students/add/", views.StudentCreateView.as_view(), name="student_add"),
    path("students/<int:pk>/edit/", views.StudentUpdateView.as_view(), name="student_edit"),
    path("students/<int:pk>/delete/", views.StudentDeleteView.as_view(), name="student_delete"),
    path("subjects/", views.SubjectListView.as_view(), name="subject_list"),
    path("subjects/add/", views.SubjectCreateView.as_view(), name="subject_add"),
    path("subjects/<int:pk>/edit/", views.SubjectUpdateView.as_view(), name="subject_edit"),
    path("subjects/<int:pk>/delete/", views.SubjectDeleteView.as_view(), name="subject_delete"),
    path("scores/", views.ScoreListView.as_view(), name="score_list"),
    path("scores/add/", views.ScoreCreateView.as_view(), name="score_add"),
    path("scores/<int:pk>/edit/", views.ScoreUpdateView.as_view(), name="score_edit"),
    path("scores/<int:pk>/delete/", views.ScoreDeleteView.as_view(), name="score_delete"),
    path("schedules/", views.ScheduleListView.as_view(), name="schedule_list"),
    path("schedules/add/", views.ScheduleCreateView.as_view(), name="schedule_add"),
    path("schedules/<int:pk>/edit/", views.ScheduleUpdateView.as_view(), name="schedule_edit"),
    path("schedules/<int:pk>/delete/", views.ScheduleDeleteView.as_view(), name="schedule_delete"),
    path("exam-schedules/", views.ExamScheduleListView.as_view(), name="exam_schedule_list"),
    path("exam-schedules/add/", views.ExamScheduleCreateView.as_view(), name="exam_schedule_add"),
    path("exam-schedules/<int:pk>/edit/", views.ExamScheduleUpdateView.as_view(), name="exam_schedule_edit"),
    path("exam-schedules/<int:pk>/delete/", views.ExamScheduleDeleteView.as_view(), name="exam_schedule_delete"),
]
