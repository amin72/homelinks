from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class ContactUs(models.Model):
    TYPES = (
        ('request', _('Request')),
        ('suggestion and recommendation', _('Suggestion and Recommendation')),
        ('advertisement', _('Advertisement')),
        ('support', _('Support')),
    )

    email = models.EmailField(verbose_name=_('Your Email'))
    text = models.TextField(max_length=1024,
        verbose_name=_('Text'),
        help_text=_("Text up to 1024 characters"))
    is_read = models.BooleanField(default=False)
    type = models.CharField(max_length=40, choices=TYPES,
        verbose_name=_('Type'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = _('Contact Us')

    def __str__(self):
        return f'{self.email}'

    def get_admin_url(self):
        model_name = self.__class__.__name__.lower()
        return reverse(f"admin:contact_{model_name}_change", args=(self.id,))
