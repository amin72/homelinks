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


def check_channel_id(channel_id, application):
    """
    Check if channel id of the `application` is correct.
    channel_id: object.channel_id
    application: object.application
    """

    # Telegram
    if application == 'telegram':
        compile = re.compile(r'^([a-zA-Z]+)([\w\d]*)([a-zA-Z0-9]+)$')
        if not compile.search(channel_id):
            raise ValidationError({'channel_id':
                _('Sorry, this name is invalid.')})

        if len(channel_id) < 5:
            raise ValidationError({'channel_id':
                _('Channel names must have at least 5 characters')})

    # Soroush
    elif application == 'soroush':
        compile = re.compile(r'^([\w\d\.]+)$')
        if not compile.search(channel_id):
            raise ValidationError({'channel_id':
                _('Sorry, this name is invalid.')})

        if len(channel_id) < 6:
            raise ValidationError({'channel_id':
                _('Channel names must have at least 6 characters')})

    # Gap
    elif application == 'gap':
        compile = re.compile(r'^([a-zA-Z]+)([\w\d]*)([a-zA-Z0-9]+)$')
        if not compile.search(channel_id):
            raise ValidationError({'channel_id':
                _('Sorry, this name is invalid.')})

        if len(channel_id) < 6:
            raise ValidationError({'channel_id':
                _('Channel names must have at least 6 characters')})

    # IGap
    elif application == 'igap':
        compile = re.compile(r'^([a-zA-Z]+)([\w\d]*)([a-zA-Z0-9]+)$')
        if not compile.search(channel_id):
            raise ValidationError({'channel_id':
                _('Sorry, this name is invalid.')})

        if len(channel_id) < 5:
            raise ValidationError({'channel_id':
                _('Channel names must have at least 5 characters')})

    # Eitaa
    elif application == 'eitaa':
        compile = re.compile(r'^([a-zA-Z0-9]+)([\w\d]*)([a-zA-Z0-9]+)$')
        if not compile.search(channel_id):
            raise ValidationError({'channel_id':
                _('Sorry, this name is invalid.')})

        if len(channel_id) < 4:
            raise ValidationError({'channel_id':
                _('Channel names must have at least 4 characters')})


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
    url = '{}{}/'.format(INSTAGRAM_LINK, self.page_id)
    return url


def check_duplicate_url(object):
    model = type(object) # get the model name
    instance = model.objects.filter(url__endswith=split_http(object.url))
    if not object.pk and instance.exists():
        if model.__name__ == 'Website':
            raise ValidationError({'url':
                _('Website already registerd')})
        elif model.__name__ == 'Channel':
            raise ValidationError({'channel_id':
                _('Channel already registerd')})
        elif model.__name__ == 'Group':
            raise ValidationError({'url':
                _('Group already registerd')})
        elif model.__name__ == 'Instagram':
            raise ValidationError({'page_id':
                _('Instagram page already registerd')})


def create_thumbnail(orig_path, thumbnail_path):
    # make two version of the image
    img = Image.open(orig_path)
    # the original one
    img.thumbnail((320, 240))
    img.save(orig_path)
    # thumbnail
    img.thumbnail((160, 120))
    img.save(thumbnail_path)
