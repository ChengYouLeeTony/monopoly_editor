# Generated by Django 3.2.5 on 2021-07-22 15:28

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0019_alter_land_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='land',
            name='color',
            field=colorfield.fields.ColorField(blank=True, choices=[('#955436', 'brown'), ('#aae0fa', 'light blue'), ('#d93a96', 'pink'), ('#f7941d', 'orange'), ('#ed1b24', 'red'), ('#fef200', 'yellow'), ('#1fb25a', 'green'), ('#0072BB', 'blue')], default='#955436', max_length=18, null=True),
        ),
    ]
