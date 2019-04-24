from django import forms
from django.utils.translation import ugettext_lazy as _
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
    type = forms.ChoiceField(label=_('Type'), choices=Report.TYPES)
    email = forms.EmailField(label=_('Email'))
    text = forms.CharField(label=_('Text'), widget=forms.Textarea,
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
