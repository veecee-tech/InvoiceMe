# Generated by Django 3.2.12 on 2022-05-31 14:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_number_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(blank=True, max_length=255, null=True)),
                ('business_address', models.CharField(blank=True, max_length=255, null=True)),
                ('business_logo', models.ImageField(blank=True, null=True, upload_to='logo/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
