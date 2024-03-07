# models.py
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils.translation import gettext_lazy as _

class Person(MPTTModel):
    GENDER_CHOICES = [
        ('male', _('Мужской')),
        ('female', _('Женский')),
    ]

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subfamilies',
        verbose_name=_("Семейная связь")
    )

    name = models.CharField(max_length=255, verbose_name=_("Имя"))
    image = models.ImageField(upload_to='image/', blank=True, null=True, verbose_name=_("Фотография"))
    birthdate = models.DateField(blank=True, null=True, verbose_name=_("Дата рождения"))
    generation = models.IntegerField(default=0, verbose_name=_("Поколение"))
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name=_("Пол"))
    
    # Добавим новые поля mid и fid
    mid = models.IntegerField(blank=True, null=True, verbose_name=_("ID мамы"))
    fid = models.IntegerField(blank=True, null=True, verbose_name=_("ID папы"))

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _("Человек")
        verbose_name_plural = _("Люди")
