# Generated by Django 3.2.5 on 2021-08-02 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0033_alter_map_cardsets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='land',
            name='description',
            field=models.CharField(blank=True, default='台北市', help_text='請輸入土地的描述', max_length=10),
        ),
        migrations.AlterField(
            model_name='userdefinevariable',
            name='player_name',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='userdefinevariablename',
            name='variable_1_name',
            field=models.CharField(blank=True, default='', help_text='請輸入自訂變數一在遊戲中的名稱', max_length=10),
        ),
        migrations.AlterField(
            model_name='userdefinevariablename',
            name='variable_2_name',
            field=models.CharField(blank=True, default='', help_text='請輸入自訂變數二在遊戲中的名稱', max_length=10),
        ),
        migrations.AlterField(
            model_name='userdefinevariablename',
            name='variable_3_name',
            field=models.CharField(blank=True, default='', help_text='請輸入自訂變數三在遊戲中的名稱', max_length=10),
        ),
        migrations.AlterField(
            model_name='userdefinevariablename',
            name='variable_4_name',
            field=models.CharField(blank=True, default='', help_text='請輸入自訂變數四在遊戲中的名稱', max_length=10),
        ),
        migrations.AlterField(
            model_name='userdefinevariablename',
            name='variable_5_name',
            field=models.CharField(blank=True, default='', help_text='請輸入自訂變數五在遊戲中的名稱', max_length=10),
        ),
    ]
