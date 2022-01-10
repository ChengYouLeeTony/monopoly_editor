# Generated by Django 3.2.5 on 2021-09-10 11:18

from django.db import migrations, models
import monopoly.models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0076_alter_backgroundsetting_tile_background_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backgroundsetting',
            name='tile_background_img',
            field=models.ImageField(blank=True, default='', null=True, upload_to=monopoly.models.map_background_path),
        ),
    ]
