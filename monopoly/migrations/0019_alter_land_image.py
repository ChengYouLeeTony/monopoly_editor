# Generated by Django 3.2.5 on 2021-07-22 10:03

from django.db import migrations, models
import monopoly.models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0018_alter_land_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='land',
            name='image',
            field=models.ImageField(default='', upload_to=monopoly.models.map_lands_path),
        ),
    ]