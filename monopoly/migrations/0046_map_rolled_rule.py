# Generated by Django 3.2.5 on 2021-08-15 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0045_alter_land_modal_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='rolled_rule',
            field=models.TextField(default="if money < 0:\n\tis_game_end = 'true'", max_length=1000),
        ),
    ]
