from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Doc(models.Model):
    STATUS_CHOICES = [
        ('P', 'Подготовка'),
        ('D', 'Доработка'),
        ('C', 'Согласование'),
        ('S', 'Подписание'),
        ('R', 'Регистрация'),
        ('A', 'Зарегистрировано'),
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
    agreementer = models.ForeignKey(
        'Person',
        on_delete=models.PROTECT,
        blank=True,
        verbose_name='Согласующий',
        related_name='agr'
    )
    signatory = models.ForeignKey(
        'Person',
        on_delete=models.PROTECT,
        related_name='sign',
        verbose_name='Подписант',
    )
    address = models.ForeignKey(
        'Institution',
        on_delete=models.PROTECT,
        verbose_name='Учреждение',
    )
    recepient = models.ForeignKey(
        'Person',
        on_delete=models.PROTECT,
        related_name='recep',
        verbose_name='Получатель'
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        verbose_name='Статус',
        blank=True, default='P'
    )
    docfile = models.FileField(
        upload_to='docs/%Y/%m/%d/',
        verbose_name='Документ',
    )
    reg_num = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Регистрационный номер'
    )
    
    def get_absolute_url(self):
        return reverse("doc_detail", kwargs={"pk": self.pk})
    
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
        verbose_name='Сотрудник',
        related_name='per'
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        verbose_name='Наименование учреждения'
    )
    can_sign = models.BooleanField(
        verbose_name='Имеет право подписи',
        default=False,
    )
    can_agree = models.BooleanField(
        verbose_name='Может согласовать',
        default=False,
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        uname = User.objects.get(pk=self.name_id)
        return f'{uname.first_name} {uname.last_name}'
