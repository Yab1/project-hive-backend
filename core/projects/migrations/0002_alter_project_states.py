# Generated by Django 5.0.6 on 2024-10-16 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='states',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Completed'), (3, 'On Hold'), (4, 'Cancelled')]),
        ),
    ]