# Generated by Django 3.2.5 on 2021-07-19 06:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('monopoly', '0003_alter_cardset_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardset',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='卡片集的獨特id', primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('map_name', models.CharField(help_text='請輸入地圖名稱', max_length=10)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='地圖的獨特id', primary_key=True, serialize=False)),
                ('cardsets', models.ManyToManyField(help_text='選擇所包含的卡片集', to='monopoly.Cardset')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
