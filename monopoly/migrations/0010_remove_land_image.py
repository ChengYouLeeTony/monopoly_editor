# Generated by Django 3.2.5 on 2021-07-21 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0009_alter_land_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='land',
            name='image',
        ),
    ]