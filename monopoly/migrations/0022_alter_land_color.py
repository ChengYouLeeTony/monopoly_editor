# Generated by Django 3.2.5 on 2021-07-22 15:35

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0021_alter_land_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='land',
            name='color',
            field=colorfield.fields.ColorField(blank=True, choices=[('#955436', 'brown'), ('#AAE0FA', 'light blue'), ('#D93A96', 'pink'), ('#F7941D', 'orange'), ('#ED1B24', 'red'), ('#FEF200', 'yellow'), ('#1FB25A', 'green'), ('#0072BB', 'blue')], default='#955436', max_length=18, null=True),
        ),
    ]
