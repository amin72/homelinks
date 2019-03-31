from copy import deepcopy
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from rest_framework.serializers import ValidationError as drf_ValidationError
from PIL import Image
from dashboard.models import Action


TELEGRAM_LINK = 'https://t.me/'
SOROUSH_LINK = 'https://sapp.ir/'
GAP_LINK = 'https://gap.im/'
IGAP_LINK = 'https://profile.igap.net/'
EITAA_LINK = 'https://eitaa.com/'
INSTAGRAM_LINK = 'https://instagram.com/'

WEBSITE_EXISTS = _('Website already exists')
CHANNEL_EXISTS = _('Channel already exists')
GROUP_EXISTS = _('Group already exists')
INSTAGRAM_EXISTS = _('Instagram page already exists')
SHORT_NAME = _('Sorry, This name is too short')
INVALID_NAME = _('Sorry, this name is invalid.')

validation_exceptions = {
    'website': ValidationError({'url': WEBSITE_EXISTS}),
    'channel': ValidationError({'channel_id': CHANNEL_EXISTS}),
    'group': ValidationError({'url': GROUP_EXISTS}),
    'instagram': ValidationError({'page_id': INSTAGRAM_EXISTS}),
}

serialize_validation_exceptions = {
    'website': drf_ValidationError({'url': WEBSITE_EXISTS}),
    'channel': drf_ValidationError({'channel_id': CHANNEL_EXISTS}),
    'group': drf_ValidationError({'url': GROUP_EXISTS}),
    'instagram': drf_ValidationError({'page_id': INSTAGRAM_EXISTS}),
}


def split_protocol(url):
    """
    Remove http://www. or https://www. from given url
    """
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


def duplicate_url(object):
    """
    Check if the url already exists.
    Return True on exiting the object else False.
    """
    model = object.__class__ # get the model name
    instance = model.objects.filter(url__endswith=split_protocol(object.url))

    if instance.exists(): # object exists
        instance = instance.first()
        if (object.parent == instance) or (object == instance):
            return False
        else:
            return True
    return False # object not found (no duplicate object)


def create_thumbnail(orig_path, thumbnail_path):
    # make two version of the image
    img = Image.open(orig_path)
    # the original one
    img.thumbnail((320, 240))
    img.save(orig_path)
    # thumbnail
    img.thumbnail((160, 120))
    img.save(thumbnail_path)


def link_updated(object, data, fields):
    # check if values are the same before and after updating
    # if none of the values changed do not create child or update it
    for field in fields: # check all form fields
        if hasattr(object, field):
            value = getattr(object, field)
            if data.get(field) != value:
                return True
    # object values are the same (link didn't get updated)
    return False


def create_or_update_action(object, type_of_action):
    link_models = ['website', 'channel', 'group', 'instagram', 'report']
    contact_models = ['contactus']

    model_name = object.model_name
    if model_name in link_models:
        content_type = ContentType.objects.get(model=model_name,
                                               app_label='links')
    elif model_name in contact_models:
        content_type = ContentType.objects.get(model=model_name,
                                               app_label='contact')

    action, created = Action.objects.get_or_create(
        type=type_of_action,
        content_type=content_type,
        object_id=object.id)

    # if action already exists (was updated before), set `is_read` to False
    if not created:
        action.is_read = False
        action.save()


def validate_and_update_link(object, data):
    # Create child if child does not exist.
    if object.parent:
        object_dup = object # update child
    else:
        object_dup = deepcopy(object) # create a child
        object_dup.pk = None
        print('saving child...')
        object_dup.save()
        object_dup.parent = object

    # Assign all values that are sent with form to child.
    # settings specific fields
    model_name = object_dup.model_name
    if model_name == 'website':
        object_dup.type = data.get('type')
        object_dup.url = data.get('url')
        domain, ext = split_protocol(object_dup.url).split('.')
        slug = f'{domain}-{ext}'
        object.slug = slugify(slug)

    elif model_name == 'channel':
        object_dup.application = data.get('application')
        object_dup.channel_id = data.get('channel_id')
        if not valid_channel_id(object_dup.channel_id,
                                      object_dup.application):
            raise ValidationError({'channel_id': INVALID_NAME_MESSAGE})
        if not valid_channel_length(object_dup.channel_id,
                                    object_dup.application):
            raise ValidationError({'channel_id': SHORT_NAME_MESSAGE})

        object_dup.url = generate_channel_url(object_dup.channel_id,
            object_dup.application)
        object_dup.slug = slugify(
            f'{object_dup.application}-{object_dup.channel_id}')

    elif model_name == 'group':
        object_dup.application = data.get('application')
        slug = \
            f'{object_dup.application}-{object_dup.title}-{object_dup.uuid}'
        self.slug = slugify(slug)

    elif model_name == 'instagram':
        object_dup.page_id = data.get('page_id')
        object_dup.url = generate_instagram_url(object_dup.page_id)
        object_dup.slug = slugify(f'{object_dup.page_id}')

    # check for duplicate url
    if duplicate_url(object_dup):
        print('not successful')
        return False # operation was not successful

    print('successful')

    # if `url` was valid, set other attributes
    object_dup.title = data.get('title')
    object_dup.category = data.get('category')
    object_dup.description = data.get('description')
    object_dup.status = 'draft'

    # save old image and thumbnail path
    old_dup_image_path = object_dup.image.path
    old_dup_thumbnail_path = object_dup.thumbnail_path
    object_dup.image = data.get('image')

    # set tags
    for tag in object.tags.all():
       object_dup.tags.set(tag)

    # save child (updated object)
    object_dup.save()
    create_or_update_action(object_dup, 'link updated')

    # remove unused image and thumbnail
    if object_dup.image.path != old_dup_image_path and \
        object.image.path != old_dup_image_path:
        os.remove(old_dup_image_path)
        os.remove(old_dup_thumbnail_path)
    return True
