import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _
from PIL import Image


WHATSAPP_LINK = 'https://chat.whatsapp.com/'
TELEGRAM_LINK = 'https://t.me/'
SOROUSH_LINK = 'https://sapp.ir/'
GAP_LINK = 'https://gap.im/'
IGAP_LINK = 'https://profile.igap.net/'
EITAA_LINK = 'https://eitaa.com/'
INSTAGRAM_LINK = 'https://instagram.com/'


def split_http(url):
    url = url.split('//')[1]
    if url.startswith('www'):
        url = url.split('.', 1)[1]
    return url


def valid_instagram_id(value):
    # regex to validate instagra username (@ striped)
    compile = re.compile(
    "^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$")
    if compile.match(value):
        return True
    return False


def valid_channel_id(channel_id, application):
    """
    Check if channel id of the `application` is correct.
    channel_id: object.channel_id
    application: object.application
    """

    if application == 'telegram':
        compile = re.compile(r'^([a-zA-Z]+)([\w\d]*)([a-zA-Z0-9]+)$')
        if compile.match(channel_id):
            return True

    elif application == 'soroush':
        compile = re.compile(r'^([\w\d\.]+)$')
        if compile.match(channel_id):
            return True

    elif application == 'gap':
        compile = re.compile(r'^([a-zA-Z]+)([\w\d]*)([a-zA-Z0-9]+)$')
        if compile.match(channel_id):
            return True

    elif application == 'igap':
        compile = re.compile(r'^([a-zA-Z]+)([\w\d]*)([a-zA-Z0-9]+)$')
        if compile.match(channel_id):
            return True

    elif application == 'eitaa':
        compile = re.compile(r'^([a-zA-Z0-9]+)([\w\d]*)([a-zA-Z0-9]+)$')
        if compile.match(channel_id):
            return True

    return False


def valid_channel_length(channel_id, application):
    channel_name_length = len(channel_id)

    if application == 'telegram':
        if channel_name_length >= 5:
            return True
    elif application == 'soroush':
        if channel_name_length >= 6:
            return True
    elif application == 'gap':
        if channel_name_length >= 6:
            return True
    elif application == 'igap':
        if channel_name_length >= 5:
            return True
    elif application == 'eitaa':
        if channel_name_length >= 4:
            return True
    return False


def generate_channel_url(channel_id, application):
    """
    Generate channel url of gives channel ID
    """

    # Telegram
    if application == 'telegram':
        url = '{}{}/'.format(TELEGRAM_LINK, channel_id)
    # Soroush
    elif application == 'soroush':
        url = '{}{}/'.format(SOROUSH_LINK, channel_id)
    # Gap
    elif application == 'gap':
        url = '{}{}/'.format(GAP_LINK, channel_id)
    # IGap
    elif application == 'igap':
        url = '{}{}/'.format(IGAP_LINK, channel_id)
    # Eitaa
    elif application == 'eitaa':
        url = '{}{}/'.format(EITAA_LINK, channel_id)
    else:
        raise ValidationError({'application':
            _('This application is not registered in the system.')})
    return url


def generate_instagram_url(page_id):
    """
    Generate instagram page url of gives page ID
    """
    url = '{}{}/'.format(INSTAGRAM_LINK, page_id)
    return url


def check_duplicate_url(object):
    """
    Check if the url already exists.
    Return True on exiting the object else False.
    """
    model = object.__class__ # get the model name
    instance = model.objects.filter(url__endswith=split_http(object.url))
    if not object.pk and instance.exists():
        return True
    else:
        return False


def create_thumbnail(orig_path, thumbnail_path):
    # make two version of the image
    img = Image.open(orig_path)
    # the original one
    img.thumbnail((320, 240))
    img.save(orig_path)
    # thumbnail
    img.thumbnail((160, 120))
    img.save(thumbnail_path)
