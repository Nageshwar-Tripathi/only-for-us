# Generated by Django 4.0 on 2022-01-13 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_polls_poll_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='polls',
            name='poll_slug',
        ),
    ]