# Generated by Django 3.2.5 on 2021-08-28 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0052_alter_chancecard_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='chancecard',
            name='money_addition',
            field=models.IntegerField(default=0, help_text='請輸入增加的金錢數目'),
        ),
    ]
