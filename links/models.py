import uuid
import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models, IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import activate
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation
)
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from taggit.managers import TaggableManager

from dashboard.models import Action
from . import utils


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Categories')
        ordering = ('order', 'name')


def image_upload_path(instance, filename):
    # define directory name
    # websites, channels, groups, instagrams
    directory = instance.__class__.__name__.lower() + 's'
    return 'images/{}/{}'.format(directory, filename)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published', parent=None)


class Link(models.Model):
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('published', _('Published')),
    )
    url_help_text = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        url = self._meta.get_field('url')
        url.help_text = self.url_help_text

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=60, verbose_name=_('Title'),
        help_text=_("Write a title for your link"))
    slug = models.SlugField(max_length=60, blank=True)
    url = models.URLField(verbose_name=_('URL'))
    category = models.ForeignKey(Category,
        on_delete=models.SET_NULL,
        verbose_name=_('Category'),
        null=True)
    description = models.TextField(max_length=500,
        verbose_name=_('Description'),
        help_text=_("Link's description up to 500 characters"))
    image = models.ImageField(upload_to=image_upload_path,
        verbose_name=_('Image'))
    created = models.DateTimeField(default=timezone.localtime)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
        default='draft')
    parent = models.ForeignKey("self", null=True, blank=True,
		on_delete=models.CASCADE)
    tags = TaggableManager()
    actions = GenericRelation(Action)

    @property
    def thumbnail_url(self):
        """Get thumbnail url"""
        image_url, ext = os.path.splitext(self.image.url)
        return image_url + '_thumbnail' + ext

    @property
    def thumbnail_path(self):
        """Get thumbnail path"""
        image_path, ext = os.path.splitext(self.image.path)
        return image_path + '_thumbnail' + ext

    def get_object_url(self, action='detail'):
        """
        Generate URL for detail, update, and delete object.
        `action`: detail, update, delete
        """
        ACTIONS = ['detail', 'update', 'delete']
        if action in ACTIONS:
            slug = self.slug
            model = self.__class__.__name__.lower()
            url_reverse = f'links:{model}-{action}'
            return reverse(url_reverse, kwargs={'slug': slug})
        raise ValueError(f"action must be one of {ACTIONS}")

    def get_absolute_url(self):
        return self.get_object_url(action='detail')

    def get_update_url(self):
        return self.get_object_url(action='update')

    def get_delete_url(self):
        return self.get_object_url(action='delete')

    def get_admin_url(self):
        model_name = self.__class__.__name__.lower()
        activate('en')
        return reverse(f"admin:links_{model_name}_change", args=(self.id,))

    @property
    def child(self):
        model = self.__class__
        return model.objects.filter(parent=self).first()

    @property
    def is_parent(self):
        """
        Object with parent=None are parent objects,
        otherwise they are children
        """
        if self.parent is not None:
            return False
        return True

    @property
    def model_name(self):
        return self.__class__.__name__.lower()

    # NOTE: exceptions in save method will be risen only in web-bse views
    # for api views we need to raise specific exceptions
    def save(self, *args, **kwargs):
        # if object has parent (object is a child)
        if self.parent and self.status == 'published':
            # hide update action once object is published
            action = self.actions.first()
            if action:
                utils.hide_action(action)

            # save parent image and thumbnail path
            old_image_path = self.parent.image.path
            old_thumbnail_path = self.parent.thumbnail_path

            parent = self.parent
            # make parent and child equal
            fields = [f.name for f in self._meta.fields]
            fields.remove('id')
            fields.remove('created')
            fields.remove('updated')
            fields.remove('parent')
            for field in fields:
                attr_self_val = getattr(self, field)
                setattr(parent, field, attr_self_val)
            parent.save()

            # if parent and child are not pointing to old images, remove them
            if self.image.path != old_image_path and \
                self.parent.image.path != old_image_path:
                os.remove(old_image_path)
                os.remove(old_thumbnail_path)

        # set slug filed
        model_name = self.__class__.__name__.lower()
        if model_name == 'website':
            # strip all characters after domain
            url = self.url.rsplit("/", self.url.count("/") - 2)[0]
            # slug: domain-extention => webiste-org, google-com
            *domain, ext = utils.split_protocol(url).split('.')
            self.slug = slugify(f'{domain}-{ext}')
        elif model_name == 'channel':
            self.slug = f'{self.application}-{self.channel_id}'
            self.url = utils.generate_channel_url(self.channel_id,
                self.application)
        elif model_name == 'group':
            self.slug = slugify(f'{self.application}-f{self.uuid}')
        elif model_name == 'instagram':
            self.slug = slugify(f'ig-{self.page_id}')
            self.url = utils.generate_instagram_url(self.page_id)

        super().save(*args, **kwargs)
        utils.scale_image(self.image.path)
        utils.create_thumbnail(self.image.path, self.thumbnail_path)

        # if object is parent and is published, hide created action
        if not self.parent and self.status == 'published':
            action = self.actions.first()
            if action:
                utils.hide_action(action)


    # Managers
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        abstract = True


class Website(Link):
    url_reverse = 'links:website-detail'
    url_help_text = _('example: https://www.google.com')

    TYPE_CHOICESS = (
        ('iranian', _('Iranian')),
        ('foreign', _('Foreign')),
    )

    type = models.CharField(max_length=7, choices=TYPE_CHOICESS,
        verbose_name=_('Type of Link'),
        help_text=_("Iranian or foreign website"))

    def __str__(self):
        return f'{self.title} - ({self.url})'

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if utils.is_duplicate_url(self):
            raise utils.validation_exceptions[self.model_name]

    class Meta:
        ordering = ('-created',)


class Channel(Link):
    url_reverse = 'links:channel-detail'

    APPLICATION_CHOICES = (
        ('telegram', _('Telegram')),
        ('soroush', _('Soroush')),
        ('gap', _('Gap')),
        ('igap', _('IGap')),
        ('eitaa', _('Eitaa')),
    )

    application = models.CharField(max_length=8, choices=APPLICATION_CHOICES,
        verbose_name=_('Application'))
    channel_id = models.CharField(max_length=32, verbose_name=_('Channel ID'),
        help_text=_('Your channel ID without @ simple'))

    def __str__(self):
        return '{} ({})'.format(self.title, self.channel_id)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if not utils.valid_channel_id(self.channel_id, self.application):
            raise ValidationError({'channel_id': utils.INVALID_NAME})

        if not utils.valid_channel_length(self.channel_id, self.application):
            raise ValidationError({'channel_id': utils.SHORT_NAME})

        self.url = utils.generate_channel_url(self.channel_id, self.application)
        if utils.is_duplicate_url(self):
            raise utils.validation_exceptions[self.model_name]

    class Meta:
        ordering = ('-created',)


class Group(Link):
    url_reverse = 'links:group-detail'
    url_help_text = \
    _('example: https://chat.whatsapp.com/46CvXH44diaHVpTRFGA55K')

    APPLICATION_CHOICES = (
        ('whatsapp', _('Whatsapp')),
        ('telegram', _('Telegram')),
        ('soroush', _('Soroush')),
        ('gap', _('Gap')),
        ('igap', _('IGap')),
        ('eitaa', _('Eitaa')),
    )

    application = models.CharField(max_length=8, choices=APPLICATION_CHOICES,
        verbose_name=_('Application'))
    # this uuid is used to prevent duplication of group slug
    uuid = models.CharField(max_length=36, default=uuid.uuid4, editable=False)

    def __str__(self):
        return '{} ({})'.format(self.title, self.url)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if utils.is_duplicate_url(self):
            raise utils.validation_exceptions[self.model_name]

    class Meta:
        ordering = ('-created',)


class Instagram(Link):
    url_reverse = 'links:instagram-detail'

    page_id = models.CharField(max_length=30, verbose_name=_('Page ID'),
        help_text=_('Your instagram ID without @ simple'))

    def __str__(self):
        return '{} ({})'.format(self.title, self.page_id)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if not utils.valid_instagram_id(self.page_id):
            raise ValidationError({'page_id': utils.INVALID_NAME})

        self.url = utils.generate_instagram_url(self.page_id)
        if utils.is_duplicate_url(self):
            raise utils.validation_exceptions[self.model_name]

    class Meta:
        ordering = ('-created',)


class Report(models.Model):
    TYPES = (
        ('inappropriate content', _('Inappropriate content')),
        ('mismatched title and description',
            _('Mismatched title and description')),
        ('broken link', _('Broken link')),
    )

    url = models.URLField(verbose_name=_('URL'))
    email = models.EmailField(verbose_name=_('Email'))
    type = models.CharField(max_length=256,
        choices=TYPES,
        verbose_name=_('Type of Report'))
    text = models.TextField(max_length=1024,
        verbose_name=_('Text'),
        help_text=_("Text up to 1024 characters"),)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    actions = GenericRelation(Action)

    # this model can manage many objects (website, groups, ...)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.content_object}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        utils.create_or_update_action(self, 'link reported')

    @property
    def model_name(self):
        return self.__class__.__name__.lower()

    def get_admin_url(self):
        model_name = self.model_name
        activate('en')
        return reverse(f"admin:links_{model_name}_change", args=(self.id,))
