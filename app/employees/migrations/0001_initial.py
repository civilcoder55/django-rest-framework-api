# Generated by Django 3.2.8 on 2021-10-14 19:39

from django.db import migrations, models
import django.db.models.deletion
import employees.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=7)),
                ('picture', models.ImageField(null=True, upload_to=employees.utils.gen_pic_file_path)),
                ('hired_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='departments.department')),
            ],
        ),
    ]
