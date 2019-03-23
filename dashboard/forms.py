from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from snowpenguin.django.recaptcha3.fields import ReCaptchaField
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
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'captcha',
        )


class UserUpdateForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'captcha',
        )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number',)
