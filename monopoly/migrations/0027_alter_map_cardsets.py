# Generated by Django 3.2.5 on 2021-07-29 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0026_alter_land_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='cardsets',
            field=models.ManyToManyField(blank=True, help_text='選擇所包含的卡片集', null=True, to='monopoly.Cardset'),
        ),
    ]
