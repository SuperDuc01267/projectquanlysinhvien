

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_student_user_schedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_date', models.DateField(verbose_name='Ngày thi')),
                ('start_time', models.TimeField(verbose_name='Giờ bắt đầu')),
                ('room', models.CharField(max_length=50, verbose_name='Phòng thi')),
                ('seat_number', models.CharField(blank=True, max_length=20, verbose_name='Số báo danh')),
                ('note', models.CharField(blank=True, max_length=255, verbose_name='Ghi chú')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_schedules', to='students.student', verbose_name='Sinh viên')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_schedules', to='students.subject', verbose_name='Môn học')),
            ],
            options={
                'verbose_name': 'Lịch thi',
                'verbose_name_plural': 'Lịch thi',
                'ordering': ['student__student_code', 'exam_date', 'start_time'],
                'constraints': [models.UniqueConstraint(fields=('student', 'subject', 'exam_date', 'start_time'), name='unique_student_exam_slot')],
            },
        ),
    ]
