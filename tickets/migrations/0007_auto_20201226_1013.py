# Generated by Django 3.1.4 on 2020-12-26 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0006_ticketassignee_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketattachment',
            name='attachment',
            field=models.FileField(upload_to='ticket_attachments'),
        ),
    ]