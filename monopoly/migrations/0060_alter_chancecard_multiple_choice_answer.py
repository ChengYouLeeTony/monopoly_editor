# Generated by Django 3.2.5 on 2021-08-30 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0059_alter_chancecard_multiple_choice_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chancecard',
            name='multiple_choice_answer',
            field=models.IntegerField(default=0),
        ),
    ]
