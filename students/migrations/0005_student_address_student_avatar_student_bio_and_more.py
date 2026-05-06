

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_schedule_effective_from_schedule_effective_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='address',
            field=models.CharField(blank=True, max_length=255, verbose_name='Dia chi'),
        ),
        migrations.AddField(
            model_name='student',
            name='avatar',
            field=models.FileField(blank=True, null=True, upload_to='avatars/', verbose_name='Anh dai dien'),
        ),
        migrations.AddField(
            model_name='student',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Gioi thieu ban than'),
        ),
        migrations.AddField(
            model_name='student',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, verbose_name='So dien thoai'),
        ),
    ]
