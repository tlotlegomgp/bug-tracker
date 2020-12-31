# Generated by Django 3.1.4 on 2020-12-31 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20201228_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectrole',
            name='user_role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Project Manager', 'Project Manager'), ('Developer', 'Developer'), ('Submitter', 'Submitter'), ('Unassigned', 'Unassigned')], default='Un-assigned', max_length=20),
        ),
    ]
