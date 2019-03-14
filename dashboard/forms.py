from django import forms
from django.utils.translation import gettext, gettext_lazy as _


class SelectLinkForm(forms.Form):
    choices = (
        ('channel', 'کانال'),
        ('group', 'گروه'),
        ('instagram', 'اینستاگرام'),
    )
    link_type = forms.ChoiceField(choices=choices, label=_('Link Type'))
