# Generated by Django 3.2.5 on 2021-08-02 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0034_auto_20210802_0538'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdefinevariable',
            name='player_index',
            field=models.IntegerField(default=0),
        ),
    ]
