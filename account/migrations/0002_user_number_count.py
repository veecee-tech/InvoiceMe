# Generated by Django 3.2.12 on 2022-04-05 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='number_count',
            field=models.IntegerField(default=0),
        ),
    ]
