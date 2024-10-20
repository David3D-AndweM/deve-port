# Generated by Django 4.2.7 on 2024-10-18 19:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("jobs", "0008_alter_jobapplication_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="jobapplication",
            name="certificates",
        ),
        migrations.RemoveField(
            model_name="jobapplication",
            name="linked_in_profile",
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="linkedIn_profile",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="nrc_copy",
            field=models.FileField(blank=True, null=True, upload_to="nrc/"),
        ),
        migrations.AlterField(
            model_name="jobapplication",
            name="applicant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="jobapplication",
            name="experience",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="jobapplication",
            name="job",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="jobs.job"
            ),
        ),
        migrations.CreateModel(
            name="Certificate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="applications/certificates/")),
                (
                    "application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="certificates",
                        to="jobs.jobapplication",
                    ),
                ),
            ],
        ),
    ]
