# Generated by Django 2.1.7 on 2019-04-17 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Your Email')),
                ('text', models.TextField(help_text='Text up to 1024 characters', max_length=1024, verbose_name='Text')),
                ('is_read', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('request', 'Request'), ('suggestion and recommendation', 'Suggestion and Recommendation'), ('advertisement', 'Advertisement'), ('support', 'Support')], max_length=40, verbose_name='Type')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Contact Us',
                'ordering': ('-created',),
            },
        ),
    ]
