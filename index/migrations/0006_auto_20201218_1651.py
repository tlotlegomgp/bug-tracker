# Generated by Django 3.1.4 on 2020-12-18 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_auto_20201218_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=35, unique=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(max_length=35),
        ),
        migrations.AlterField(
            model_name='ticketattachment',
            name='note',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='ticketcomment',
            name='body_message',
            field=models.CharField(max_length=100),
        ),
    ]