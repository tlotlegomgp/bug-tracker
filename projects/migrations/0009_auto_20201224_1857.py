# Generated by Django 3.1.4 on 2020-12-24 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20201224_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectrole',
            name='user_role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('MAN', 'Project Manager'), ('SUB', 'Submitter'), ('DEV', 'Developer')], default='DEV', max_length=20),
        ),
    ]
