# Generated by Django 5.1.4 on 2025-01-02 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_project_remove_userinteraction_contact_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='category',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='link',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
