# Generated by Django 3.2.5 on 2021-08-06 15:20

from django.db import migrations, models
import monopoly.models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0036_auto_20210802_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='land',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, upload_to=monopoly.models.map_lands_path),
        ),
    ]
