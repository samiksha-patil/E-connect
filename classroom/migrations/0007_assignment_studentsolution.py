# Generated by Django 3.0.6 on 2020-05-09 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classroom', '0006_auto_20200508_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to='assignments/')),
                ('description', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment', to='classroom.Teachercreate')),
            ],
        ),
        migrations.CreateModel(
            name='Studentsolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to='assignmets/solution')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sol_assignment', to='classroom.Assignment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]