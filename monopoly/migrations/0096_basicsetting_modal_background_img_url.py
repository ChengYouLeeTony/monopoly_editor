# Generated by Django 3.2.5 on 2021-10-25 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0095_cardset_background_img_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicsetting',
            name='modal_background_img_url',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]
