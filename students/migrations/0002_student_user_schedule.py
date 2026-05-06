

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_profile', to=settings.AUTH_USER_MODEL, verbose_name='Tài khoản đăng nhập'),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.CharField(choices=[('2', 'Thứ 2'), ('3', 'Thứ 3'), ('4', 'Thứ 4'), ('5', 'Thứ 5'), ('6', 'Thứ 6'), ('7', 'Thứ 7'), ('CN', 'Chủ nhật')], max_length=2, verbose_name='Thứ')),
                ('room', models.CharField(max_length=50, verbose_name='Phòng học')),
                ('start_time', models.TimeField(verbose_name='Giờ bắt đầu')),
                ('end_time', models.TimeField(verbose_name='Giờ kết thúc')),
                ('note', models.CharField(blank=True, max_length=255, verbose_name='Ghi chú')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='students.student', verbose_name='Sinh viên')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='students.subject', verbose_name='Môn học')),
            ],
            options={
                'verbose_name': 'Thời khóa biểu',
                'verbose_name_plural': 'Thời khóa biểu',
                'ordering': ['student__student_code', 'weekday', 'start_time'],
                'constraints': [models.UniqueConstraint(fields=('student', 'subject', 'weekday', 'start_time'), name='unique_student_schedule_slot')],
            },
        ),
    ]
