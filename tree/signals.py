from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from tree.models import Person


@receiver(m2m_changed, sender=Person.pids.through)
def update_partner(sender, instance, action, **kwargs):
    if action == 'post_add' and 'pk_set' in kwargs:
        partner_pks = kwargs['pk_set']
        for partner_pk in partner_pks:
            partner = Person.objects.get(pk=partner_pk)
            partner.pids.add(instance)
            instance.pids.add(partner)
