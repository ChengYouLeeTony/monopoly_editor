# Generated by Django 3.2.5 on 2021-07-26 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0024_auto_20210724_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='land',
            name='description',
            field=models.CharField(blank=True, default='台北市', help_text='請輸入土地的描述', max_length=10, null=True),
        ),
    ]
