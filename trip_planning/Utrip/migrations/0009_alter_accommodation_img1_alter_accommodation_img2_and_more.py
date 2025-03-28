# Generated by Django 5.0.6 on 2025-03-16 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Utrip', '0008_type_transportation_tripproposal_accommodation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accommodation',
            name='img1',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/pics_rooms'),
        ),
        migrations.AlterField(
            model_name='accommodation',
            name='img2',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/pics_rooms'),
        ),
        migrations.AlterField(
            model_name='destination',
            name='featured_img',
            field=models.ImageField(upload_to='pictures/pics'),
        ),
        migrations.AlterField(
            model_name='destination',
            name='img1',
            field=models.ImageField(upload_to='pictures/pics'),
        ),
        migrations.AlterField(
            model_name='destination',
            name='img2',
            field=models.ImageField(upload_to='pictures/pics'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pictures/default.jpg', upload_to='pictures/profile_pictures/'),
        ),
        migrations.AlterField(
            model_name='transportation',
            name='img1',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/pics_vehicle'),
        ),
        migrations.AlterField(
            model_name='transportation',
            name='img2',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/pics_vehicle'),
        ),
    ]
