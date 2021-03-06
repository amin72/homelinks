import re

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_text
from django.urls import reverse
from rest_framework.authtoken.models import Token


def phone_number_validator(value):
    """
    A phone validator
    """
    if value:
        regex= re.compile('09(0[1-5]|1[0-9]|3[0-9]|2[0-2])-?[0-9]{3}-?[0-9]{4}')
        result = regex.search(value)
        if result is None:
            raise ValidationError(_('Enter a valid phone number'))


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name=_('Email'))

    phone_number = models.CharField(max_length=11, blank=True, null=True,
        unique=True, verbose_name=_('Phone Number'),
        validators=[phone_number_validator],
        help_text=_('User Phone Number, example: 09123456790 (Optional)'))
    is_premium = models.BooleanField(default=False, verbose_name=_('Premium'))


@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Action(models.Model):
    TYPES_OF_ACTIONS = (
        ('link created', _('Link Created')),
        ('link updated', _('Link Updated')),
        ('link reported', _('Link Reported')),
        ('contact_us', _('Contact Us')),
    )

    type = models.CharField(max_length=20, verbose_name=_('Type of Action'),
        choices=TYPES_OF_ACTIONS)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # this model can manage many objects (report, website, groups, ...)
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('content type'),
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(_('object id'), db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        return f'{smart_text(self.content_object)}'

    def get_admin_url(self):
        model_name = self.__class__.__name__.lower()
        return reverse(f"admin:dashboard_{model_name}_change", args=(self.id,))
