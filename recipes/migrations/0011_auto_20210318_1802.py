# Generated by Django 2.2 on 2021-03-18 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20210318_1408'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='dimension',
            new_name='unit',
        ),
    ]
