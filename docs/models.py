from django.db import models
from django.contrib.auth.models import User


class Doc(models.Model):
    STATUS_CHOICES = [
        ('P', 'Подготовка'),
        ('C', 'Согласование'),
        ('S', 'Подписание'),
        ('R', 'Регистрация'),
        ('A', 'Отправлено'),
    ]
    title = models.CharField(
        max_length=150,
        verbose_name='Краткое содержание',
    )
    user = models.ForeignKey(
        'Person', on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name='Исполнитель',
        related_name='exe'
    )
    reg_num = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Регистрационный номер'
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        verbose_name='Статус',
        blank=True, default='P'
    )
    docfile = models.FileField(
        blank=True,
        upload_to='docs/%Y/%m/%d/',
        verbose_name='Документ',
    )
    signatory = models.ForeignKey(
        'Person',
        on_delete=models.PROTECT,
        blank=True,
        related_name='sign',
        verbose_name='Подписант',
        default=None,
    )

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class Institution(models.Model):
    title = models.CharField(
        max_length=150, verbose_name='Наименование учреждения')

    class Meta:
        verbose_name = 'Учреждение'
        verbose_name_plural = 'Учреждения'

    def __str__(self):
        return self.title


class Person(models.Model):
    name = models.OneToOneField(
        User, on_delete=models.PROTECT,
        verbose_name='Сотрудник'
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        verbose_name='Наименование учреждения'
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        uname = User.objects.get(pk=self.name_id)
        return f'{uname.first_name} {uname.last_name}'
