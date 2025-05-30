# Generated by Django 5.1.3 on 2024-12-22 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0010_alter_appointment_service_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('medications', models.TextField(blank=True, null=True)),
                ('complaints', models.TextField(blank=True, null=True)),
                ('allergies', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
