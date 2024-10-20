# Generated by Django 4.2.7 on 2024-10-18 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0005_alter_job_job_nature"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="location",
            field=models.CharField(
                choices=[
                    ("Chingola", "Chingola"),
                    ("Lusaka", "Lusaka"),
                    ("Kitwe", "Kitwe"),
                    ("Ndola", "Ndola"),
                    ("Livingstone", "Livingstone"),
                    ("Luanshya", "Luanshya"),
                    ("Mufulira", "Mufulira"),
                    ("Kabwe", "Kabwe"),
                    ("Solwezi", "Solwezi"),
                    ("Chipata", "Chipata"),
                    ("Choma", "Choma"),
                    ("Siavonga", "Siavonga"),
                    ("Mansa", "Mansa"),
                    ("Kasama", "Kasama"),
                ],
                default="Chingola",
                max_length=150,
                verbose_name="Location",
            ),
        ),
        migrations.AlterField(
            model_name="job",
            name="salary",
            field=models.FloatField(
                help_text="Salary in Zambian Kwacha", verbose_name="Salary (ZMW)"
            ),
        ),
    ]
