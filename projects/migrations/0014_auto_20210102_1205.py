# Generated by Django 3.1.4 on 2021-01-02 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_auto_20201231_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectrole',
            name='user_role',
            field=models.CharField(choices=[('Project Manager', 'Project Manager'), ('Developer', 'Developer'), ('Submitter', 'Submitter'), ('Unassigned', 'Unassigned')], default='Un-assigned', max_length=20),
        ),
    ]
