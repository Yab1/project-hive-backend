# Generated by Django 5.0.6 on 2024-10-24 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_alter_project_options_remove_project_stared_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
