# Generated by Django 3.2 on 2023-07-30 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_alter_serviceprice_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='serviceprice',
            options={'ordering': ('-sort_position',), 'verbose_name': 'Услуга', 'verbose_name_plural': 'Услуги'},
        ),
    ]