from django import forms
from django.utils.translation import gettext, ugettext as _
from .models import Report


class ReportForm(forms.Form):
    url = forms.URLField(
        label=_('Reported Link'),
        widget=forms.HiddenInput)
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_slug = forms.CharField(widget=forms.HiddenInput)
    type = forms.ChoiceField(choices=Report.TYPES)
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea)
