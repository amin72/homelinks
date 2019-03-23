from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField
)
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from snowpenguin.django.recaptcha2.widgets import ReCaptchaHiddenInput
from .models import Profile


User = get_user_model()


class SelectLinkForm(forms.Form):
    choices = (
        ('website', _('Website')),
        ('channel', _('Channel')),
        ('group', _('Group')),
        ('instagram', _('Instagram')),
    )
    link_type = forms.ChoiceField(choices=choices, label=_('Link Type'))


class UserRegisterForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaHiddenInput())

    class Meta:
        model = User
        # add  `captcha` field
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'captcha',
        )


class UserUpdateForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaHiddenInput())

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'captcha'
        )


class ProfileUpdateForm(forms.ModelForm):
    #captcha = ReCaptchaField(widget=ReCaptchaHiddenInput())

    class Meta:
        model = Profile
        fields = ('phone_number',)
