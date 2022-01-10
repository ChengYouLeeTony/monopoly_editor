# Generated by Django 3.2.5 on 2021-09-08 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0068_musicsetting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicsetting',
            name='background',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='musicsetting',
            name='dice',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='musicsetting',
            name='hover_button',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='musicsetting',
            name='money_addition',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='musicsetting',
            name='money_deduction',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='musicsetting',
            name='player_move',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='musicsetting',
            name='player_teleport',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='musicsetting',
            name='player_turn_over',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='musicsetting',
            name='user_define_1',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='musicsetting',
            name='user_define_2',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='musicsetting',
            name='user_define_3',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]