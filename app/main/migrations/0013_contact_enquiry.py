# Generated by Django 5.1.4 on 2025-01-15 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_rename_installation_address_cctv_enquiry_installation_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='contact_enquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Full Name')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('service_type', models.CharField(choices=[('solar', 'Solar'), ('cctv', 'CCTV'), ('other', 'Other')], default='other', max_length=10, verbose_name='Service Type')),
                ('additional_comments', models.TextField(blank=True, verbose_name='Additional Comments')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
