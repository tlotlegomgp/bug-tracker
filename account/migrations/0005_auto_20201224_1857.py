# Generated by Django 3.1.4 on 2020-12-24 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20201220_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='profile_images', verbose_name=''),
        ),
    ]