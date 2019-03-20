# Generated by Django 2.1.7 on 2019-03-20 11:15

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.CustomTaggedItem', to='taggit.CustomTag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='group',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.CustomTaggedItem', to='taggit.CustomTag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='instagram',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.CustomTaggedItem', to='taggit.CustomTag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='website',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.CustomTaggedItem', to='taggit.CustomTag', verbose_name='Tags'),
        ),
    ]