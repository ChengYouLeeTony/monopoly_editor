# Generated by Django 3.2.5 on 2021-12-01 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0106_auto_20211201_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicsetting',
            name='house_construction_cost',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='basicsetting',
            name='money_pass_start',
            field=models.IntegerField(default=2000),
        ),
    ]
