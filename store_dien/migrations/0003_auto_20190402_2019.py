# Generated by Django 2.1.2 on 2019-04-02 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_dien', '0002_auto_20190402_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='good_status',
            field=models.TextField(choices=[('Hàng mới', 'Hàng mới'), ('Hàng đã qua sử dụng', 'Hàng đã qua sử dụng')], verbose_name='Tình trạng vật tư'),
        ),
    ]
