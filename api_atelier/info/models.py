from django.db import models


class ServicePrice(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название услуги')
    ot = models.BooleanField(verbose_name='Добавить предлог "от" к цене')
    price = models.IntegerField(verbose_name='Стоимость услуги', default=True)
    sort_position = models.SmallIntegerField(
        verbose_name='Номер позиции', unique=True)

    class Meta:
        ordering = ('-sort_position', )
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Bot(models.Model):
    username = models.CharField(max_length=150, verbose_name='Имя бота')
    token = models.CharField(max_length=150, verbose_name='Токен для api')
    active = models.BooleanField(
        verbose_name='Является активным(должен быть единственным)',
        default=False
    )

    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Боты'
