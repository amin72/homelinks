# Generated by Django 2.1.7 on 2019-03-28 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20190326_1326'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'ordering': ('-updated',)},
        ),
        migrations.AddField(
            model_name='action',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
