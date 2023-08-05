# Generated by Django 3.2 on 2023-07-26 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_alter_serviceprice_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, verbose_name='Имя бота')),
                ('token', models.CharField(max_length=150, verbose_name='Токен для api')),
            ],
        ),
        migrations.AlterModelOptions(
            name='serviceprice',
            options={'ordering': ('-sort_position',), 'verbose_name': 'Услуга', 'verbose_name_plural': 'Услуги'},
        ),
    ]
