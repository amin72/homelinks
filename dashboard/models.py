import re

from django.db import models
from django.conf import settings
from django.utils.translation import gettext, gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


def phone_number_validator(value):
    """
    A phone validator
    """
    if value:
        regex = re.compile('09(0[1-5]|1[0-9]|3[0-9]|2[0-2])-?[0-9]{3}-?[0-9]{4}')
        result = regex.search(value)
        if result is None:
            raise ValidationError(_('Enter a valid phone number'))


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, blank=True, null=True,
        unique=True, verbose_name=_('Phone Number'),
        validators=[phone_number_validator],
        help_text=_('User Phone Number, example: 09123456790 (Optional)'))
    vip = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
