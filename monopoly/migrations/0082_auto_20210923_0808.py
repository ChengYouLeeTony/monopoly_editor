# Generated by Django 3.2.5 on 2021-09-23 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0081_rename_hoouse_construction_cost_basicsetting_house_construction_cost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basicsetting',
            name='hotel_construction_cost',
        ),
        migrations.RemoveField(
            model_name='basicsetting',
            name='ratio_rent_to_price_for_hotel',
        ),
        migrations.RemoveField(
            model_name='basicsetting',
            name='ratio_rent_to_price_for_house',
        ),
        migrations.AddField(
            model_name='basicsetting',
            name='ratio_rent_vs_price',
            field=models.FloatField(default=0.25),
        ),
        migrations.AddField(
            model_name='basicsetting',
            name='ratio_rent_vs_price_for_house',
            field=models.FloatField(default=0.25),
        ),
        migrations.AddField(
            model_name='basicsetting',
            name='rent_constant',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='basicsetting',
            name='money_initial',
            field=models.IntegerField(default=1500),
        ),
        migrations.AlterField(
            model_name='basicsetting',
            name='money_pass_start',
            field=models.IntegerField(default=200),
        ),
    ]
