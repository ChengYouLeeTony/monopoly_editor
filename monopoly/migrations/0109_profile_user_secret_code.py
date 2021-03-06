# Generated by Django 3.2.5 on 2021-12-19 19:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0108_alter_basicsetting_money_pass_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_secret_code',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='使用者用來提供遊戲觀看權的密碼'),
        ),
    ]
