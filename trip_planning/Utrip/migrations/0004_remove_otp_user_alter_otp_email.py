# Generated by Django 5.1.7 on 2025-05-05 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Utrip", "0003_otp_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="otp",
            name="user",
        ),
        migrations.AlterField(
            model_name="otp",
            name="email",
            field=models.EmailField(max_length=254),
        ),
    ]
