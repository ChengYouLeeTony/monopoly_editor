# Generated by Django 3.2.5 on 2021-08-30 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0053_chancecard_money_addition'),
    ]

    operations = [
        migrations.AddField(
            model_name='chancecard',
            name='is_multiple_choice',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chancecard',
            name='multiple_choice_1',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='chancecard',
            name='multiple_choice_2',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='chancecard',
            name='multiple_choice_3',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='chancecard',
            name='multiple_choice_4',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]