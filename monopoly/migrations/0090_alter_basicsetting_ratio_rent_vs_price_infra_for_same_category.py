# Generated by Django 3.2.5 on 2021-10-04 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0089_basicsetting_ratio_rent_vs_price_infra_for_same_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicsetting',
            name='ratio_rent_vs_price_infra_for_same_category',
            field=models.FloatField(default=0),
        ),
    ]