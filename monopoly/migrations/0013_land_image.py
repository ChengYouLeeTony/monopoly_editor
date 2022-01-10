# Generated by Django 3.2.5 on 2021-07-21 12:41

from django.db import migrations, models
import monopoly.models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0012_remove_land_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='land',
            name='image',
            field=models.ImageField(default='-1.png', upload_to=monopoly.models.map_lands_path),
        ),
    ]
