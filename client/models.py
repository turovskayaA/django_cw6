from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class ServiceClient(models.Model):
    """
    Модель клиента сервиса, который получает рассылки
    """
    email = models.EmailField(unique=True, verbose_name='Почта')
    full_name = models.CharField(max_length=250, verbose_name='ФИО')
    comment = models.CharField(max_length=150, verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        verbose_name = 'Клиент сервиса'
        verbose_name_plural = 'Клиенты сервисов'
        ordering = ('full_name',)


class Message(models.Model):
    topic = models.CharField(max_length=100, verbose_name='Тема письма')
    message = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.topic}'

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылок'


class Newsletter(models.Model):
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'

    STATUSES = (
        (STATUS_CREATED, 'Запущена'),
        (STATUS_STARTED, 'Создана'),
        (STATUS_DONE, 'Завершена'),
    )

    start_time = models.DateTimeField(verbose_name='Время старта')
    end_time = models.DateTimeField(verbose_name='Время окончания', **NULLABLE)
    period = models.CharField(max_length=20, choices=PERIODS, default=PERIOD_DAILY, verbose_name='Период')
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_CREATED, verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)
    client = models.ManyToManyField(ServiceClient, related_name='newsletter', verbose_name='Клиент')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)
    is_activated = models.BooleanField(default=True, verbose_name='Активная')

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('status',)

        permissions = [
            ('set_is_activated', 'Может отключать рассылку')
        ]


class Logi(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )

    last = models.DateTimeField(auto_now_add=True, verbose_name='Дата последней попытки')
    settings = models.ForeignKey(Newsletter, on_delete=models.SET_NULL, verbose_name='Настройки', **NULLABLE)
    status = models.CharField(choices=STATUSES, default=STATUS_OK, verbose_name='Статус')
    client = models.ForeignKey(ServiceClient, on_delete=models.SET_NULL, verbose_name='Клиент', **NULLABLE)

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'


