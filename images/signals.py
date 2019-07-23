from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image

# so function is only call if m2m_changed signals launch by sender
# django signals are asycorn and blocking don't confuse djanog signals with asycronst task
@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()
