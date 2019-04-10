from django import forms
from django.utils.translation import gettext, ugettext as _
from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from .models import (
    Website,
    Channel,
    Group,
    Instagram,
    Report,
)


class ReportForm(forms.Form):
    url = forms.URLField(
        label=_('Reported Link'),
        widget=forms.HiddenInput)
    type = forms.ChoiceField(choices=Report.TYPES)
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea,
        help_text=_("Text up to 1024 characters"))
    captcha = ReCaptchaField()


class CreateWebsiteForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Website
        fields = (
            'title',
            'url',
            'type',
            'category',
            'description',
            'image',
            'captcha',
        )


class CreateChannelForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Channel
        fields = (
            'application',
            'title',
            'channel_id',
            'category',
            'description',
            'image',
            'captcha',
        )


class CreateGroupForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Group
        fields = (
            'application',
            'title',
            'url',
            'category',
            'description',
            'image',
            'captcha',
        )


class CreateInstagramForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Instagram
        fields = (
            'title',
            'page_id',
            'category',
            'description',
            'image',
            'captcha',
        )
