# Generated by Django 5.0.6 on 2025-03-17 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Utrip', '0012_remove_accommodation_map'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accommodation',
            name='owner',
            field=models.CharField(max_length=50),
        ),
    ]
