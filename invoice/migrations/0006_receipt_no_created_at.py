# Generated by Django 3.2.12 on 2022-04-05 12:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_alter_receipt_no_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt_no',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
