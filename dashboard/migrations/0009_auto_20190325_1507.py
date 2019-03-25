# Generated by Django 2.1.7 on 2019-03-25 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20190324_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='type',
            field=models.CharField(choices=[('link created', 'Link Created'), ('link updated', 'Link Updated'), ('link reported', 'Link Reported')], max_length=20, verbose_name='Type of Action'),
        ),
    ]