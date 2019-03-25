from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from .models import ContactUs


class ContactUsForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = ContactUs
        fields = (
            'email',
            'type',
            'text',
            'captcha',
        )
