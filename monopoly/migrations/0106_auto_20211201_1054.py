# Generated by Django 3.2.5 on 2021-12-01 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0105_auto_20211030_0511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicsetting',
            name='house_construction_cost',
            field=models.CharField(default='1000', max_length=30),
        ),
        migrations.AlterField(
            model_name='basicsetting',
            name='money_pass_start',
            field=models.CharField(default='2000', max_length=30),
        ),
    ]