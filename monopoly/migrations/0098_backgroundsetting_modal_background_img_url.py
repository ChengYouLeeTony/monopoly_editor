# Generated by Django 3.2.5 on 2021-10-26 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0097_auto_20211025_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='backgroundsetting',
            name='modal_background_img_url',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]