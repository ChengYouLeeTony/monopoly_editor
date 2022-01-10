# Generated by Django 3.2.5 on 2021-10-27 11:29

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0101_auto_20211027_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backgroundsetting',
            name='land_background_color',
            field=colorfield.fields.ColorField(blank=True, default='#cde6d0', max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name='backgroundsetting',
            name='land_text_color',
            field=colorfield.fields.ColorField(blank=True, default='#000000', max_length=18, null=True),
        ),
    ]
