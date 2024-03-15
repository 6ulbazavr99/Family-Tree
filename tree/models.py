from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils.translation import gettext_lazy as _


class Person(MPTTModel):
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subfamilies',
        verbose_name=_("Семейная связь")
    )

    name = models.CharField(max_length=255, verbose_name=_("Имя"))
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Заголовок"))
    img = models.ImageField(upload_to='image/', blank=True, null=True, verbose_name=_("Фотография"))
    birthdate = models.DateField(blank=True, null=True, verbose_name=_("Дата рождения"))

    GENDER_CHOICES = [
        ('male', _('Мужской')),
        ('female', _('Женский'))
    ]
    gender = models.CharField(_('Пол'), max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    pids = models.ManyToManyField('Person', related_name='person_pids', blank=True, verbose_name=_('Партнер'))
    fid = models.ForeignKey('Person', null=True, blank=True, verbose_name=_('Отец'), on_delete=models.SET_NULL,
                            related_name='person_fids')
    mid = models.ForeignKey('Person', null=True, blank=True, verbose_name=_('Мать'), on_delete=models.SET_NULL,
                            related_name='person_mids')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _("Человек")
        verbose_name_plural = _("Люди")
