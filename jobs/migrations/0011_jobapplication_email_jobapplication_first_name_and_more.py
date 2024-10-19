# Generated by Django 4.2.7 on 2024-10-19 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0010_jobapplication_canceled_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobapplication",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="first_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="last_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
